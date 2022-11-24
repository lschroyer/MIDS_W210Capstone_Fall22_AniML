from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import altair as alt

import pandas as pd
import logging
import matplotlib.pyplot as plt
import dataframe_image as dfi


from static import random_script
import os, shutil


# setup loggers
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

cwd = os.getcwd()
logger.info(cwd)

def parse_yolo_json(yolo_json_path):
    '''
    Function to parse YOLOv5 prediction JSON files.
    Input:
    - yolo_json_path: String. Path to JSON file from YOLOv5 detection run.
    Outputs:
    - image_ids: List of strings. A list of images with detected objects. If an image has multiple objects detected, the image name will be duplicated in the list.
    - pred_classes: List of ints. A list of ints, corresponding to the classes annotated on the images in RoboFlow.
    - bboxes: List of lists. A list of bounding boxes for each detected object. Each sub-list is a list of four floats, denoting coordinates for the corners of the bounding boxes.
    - confs: List of floats. A list of confidence scores for each prediction.
    '''
    
    # reading in json file
    with open(yolo_json_path, 'r') as pred_json:
        yolo_preds = json.load(pred_json)
        # print(yolo_preds)
    
    # parsing information from json files:
    # image id's (list of strings)
    image_ids = [pred.get("image_id") for pred in yolo_preds]
    # predicted classes (list of ints)
    pred_classes = [pred.get("category_id") for pred in yolo_preds]
    # bounding boxes (list of lists, sublists are lists of floats (normalized coords))
    bboxes = [pred.get("bbox") for pred in yolo_preds]
    # confidence scores (list of floats)
    confs = [pred.get("score") for pred in yolo_preds]

    return image_ids, pred_classes, bboxes, confs

def make_class_chart(pred_df, width=300, height=600):
    '''
    Function to parse DataFrame of model predictions and create an Altair/Vega-Lite histogram of confidence levels.
    Input:
    - pred_df: Pandas DataFrame, containing at least a column "predicted classes original"
    - width: width of histogram image. Default 400.
    - height: height of histogram image. Default 600.
    Output:
    - class_chart: Altair Chart object of a histogram of predicted classes.
    '''
    if 'predicted_classes_new' in pred_df.columns:
        pred_df['predicted_classes_original'] = pred_df['predicted_classes_new']
        pred_df = pred_df.drop('predicted_classes_new', axis=1)

    
    # defining altair chart and saving as JSON
    class_chart = alt.Chart(pred_df).mark_bar().encode(
        x = alt.X("predicted_classes_original:N", title="Predicted Class"),
        y = alt.Y("count():Q", title="Count"),
        color = alt.Color("predicted_classes_original:N", scale=alt.Scale(scheme="category10"), title = "Predicted Class"),
        tooltip = [alt.Tooltip("predicted_classes_original:N", title="Predicted Class"),
                   alt.Tooltip("count():Q", title="Count")]
    ).properties(
        width = width,
        height = height,
        title = "Counts of Predicted Classes"
    )
    
    return class_chart


def make_conf_chart(pred_df, width=600, height=600):
    '''
    Function to parse DataFrame of model predictions and create an Altair/Vega-Lite histogram of confidence levels.
    Input:
    - pred_df: Pandas DataFrame, containing columns ["predicted classes original", "confidence scores"]
    - width: width of histogram image. Default 400.
    - height: height of histogram image. Default 600.
    Output:
    - conf_chart: Altair Chart object of a histogram of confidence scores.
    '''
    if 'predicted_classes_new' in pred_df.columns:
        pred_df['predicted_classes_original'] = pred_df['predicted_classes_new']
        pred_df = pred_df.drop('predicted_classes_new', axis=1)

    # defining altair chart and saving as JSON
    conf_chart = alt.Chart(pred_df).mark_bar().encode(
        x = alt.X("confidence_scores:Q", bin=alt.Bin(maxbins=10), title="Predicted Class"),
        y = alt.Y("count():Q", title="Count"),
        color = alt.Color("predicted_classes_original:N", scale=alt.Scale(scheme="category10"), title = "Predicted Class"),
        tooltip = [alt.Tooltip("confidence_scores:Q", bin=alt.Bin(maxbins=10), title="Confidence Interval"),
                   alt.Tooltip("predicted_classes_original:N", title="Predicted Class"),
                   alt.Tooltip("count()", title="Count")]
    ).properties(
        width = width,
        height = height,
        title = "Histogram of Confidence Levels"
    )
    
    return conf_chart

def time_series(pred_df):
    '''
    Function to parse dates and create time-series data from the dates in image names.
    Input:
    - pred_df: pandas DataFrame of YOLOv5 prediction results
    Outputs:
    - date_chart_total: Altair Chart object of a time-series of total detected animals.
    - date_chart_class: Altair Chart object of time-series for detected animals of each class in pred_df.
    '''
    if 'predicted_classes_new' in pred_df.columns:
        pred_df['predicted_classes_original'] = pred_df['predicted_classes_new']
        pred_df = pred_df.drop('predicted_classes_new', axis=1)


    # retrieving date from first four digits of image names in dataframe
    # appended 2022 for convenience but we won't use the year in the time series
    dates = pred_df["image_ids"].apply(lambda x: x[:4]+"2022")
    pred_df["image_ids"] = pd.to_datetime(dates, format="%m%d%Y")
    # adding date as its own column
    pred_df["image_ids"] = pd.to_datetime(dates, format="%m%d%Y")
    
    # grouping by date, imputing missing dates, and flattening dataframe for altair chart
    # this dataframe separates by predicted animal class
    date_df = pred_df.groupby(["image_ids", "predicted_classes_original"]).size().unstack(fill_value=0).reset_index()
    date_df = date_df.set_index("image_ids").asfreq("D", fill_value=0).reset_index()
    date_df_flat = pd.melt(date_df, id_vars=["image_ids"])
    
    # further aggregating to calculate total animal counts, summing by predicted class
    date_df_total = date_df_flat.drop(["predicted_classes_original"], axis=1).groupby(["image_ids"]).agg(["sum"])
    date_df_total.columns = date_df_total.columns.get_level_values(0)
    date_df_total.reset_index(inplace=True)
    
    # time-series chart for total detected animals in the dataset
    date_chart_total = alt.Chart(date_df_total).mark_line(point=True, strokeWidth=2).encode(
        x = alt.X("monthdate(image_ids):T", title = "Image Date"),
        y = alt.Y("value:Q", title = "Count of Detected Animals"),
        tooltip = [alt.Tooltip("monthdate(image_ids)", title = "Image Date"),
                   alt.Tooltip("value:Q", title = "Count of Detected Animals")]
    ).configure_point(
        size = 100
    ).properties(
        width = 1000,
        height = 300,
        title = "Total Detected Animals Time Series"
    )
    
    # creating concatenated time-series charts for each animal class detected in the dataset
    date_chart_class = alt.Chart(date_df_flat).mark_line(point=True, strokeWidth=2).encode(
        column = alt.Column("predicted_classes_original:N", title = "Predicted Animal Type"),
        x = alt.X("monthdate(image_ids):T", title = "Image Date"),
        y = alt.Y("value:Q", title = "Count of Detected Animals"),
        color = alt.Color("predicted_classes_original:N", scale=alt.Scale(scheme="category10"), title="Predicted Animal Type"),
        tooltip = [alt.Tooltip("monthdate(image_ids)", title = "Image Date"),
                   alt.Tooltip("predicted_classes_original", title = "Animal Type"),
                   alt.Tooltip("value", title = "Count of Detected Animals")]
    ).configure_point(
        size = 100
    ).properties(
        width = 450,
        height = 300,
        title = "Detected Animals Time Series by Animal Type"
    )
    
    return date_chart_total, date_chart_class


test_yolo_image_ids, test_yolo_pred_classes, test_yolo_bboxes, test_yolo_confs = parse_yolo_json("../data/classification_prediction/yolo_v5_prediction.json")

test_yolo_pred_classes_new = test_yolo_pred_classes.copy()

def filter_low_conf_images(conf_level):
    for index, image_id in enumerate(test_yolo_image_ids):
        if test_yolo_confs[index] < conf_level:
            test_yolo_pred_classes_new[index] = 0
        else:
            test_yolo_pred_classes_new[index] = 1
    return test_yolo_pred_classes_new

@router.get("/analytics", response_class=HTMLResponse)
def form_get(request: Request):
    # logger.info(cwd)
    # logger.info(test_yolo_image_ids)
    model_predictions = {"image_ids": test_yolo_image_ids, 
            "confidence_scores": test_yolo_confs, 
            "predicted_classes_original": test_yolo_pred_classes}

    df = pd.DataFrame.from_dict(model_predictions)
    df_export = df.copy()
    df_export.loc[df_export["predicted_classes_original"] == 1, "predicted_classes_original"] = "animal detected"
    df_export.loc[df_export["predicted_classes_original"] == 0, "predicted_classes_original"] = "animal not detected"
    dfi.export(df_export,"static/images/analytics/data_frame/conf_table_initial.png")
    

    ## Class 0 ##
    file_names_class_0 = df[df.predicted_classes_original == 0][["image_ids"]].values.tolist()
    # for col in model_predictions_df.columns:
    #     logger.info(col)
    # logger.info(file_names_class_0)

    # Clear files in classification folders
    destination_folder = "static/images/analytics/predicted_0/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/analytics/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_0]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    ## Class 1 ##
    file_names_class_1 = df[df.predicted_classes_original == 1][["image_ids"]].values.tolist()

    # Clear files in classification folders
    destination_folder = "static/images/analytics/predicted_1/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/analytics/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_1]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    # save outputs
    _zip_files()

    # Get random images
    random_files_names = random_files()

    # creating Altair charts from model predictions
    conf_chart = make_conf_chart(df)
    class_chart = make_class_chart(df)
    time_series_total, time_series_class = time_series(df)
    time_series_total_json = time_series_total.to_json()
    time_series_class_json = time_series_class.to_json()
    
    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(y="shared")
    concat_chart_json = concat_chart.to_json()


    model_cutoff = "default model prediction"
    show_model_table_initial = False
    return templates.TemplateResponse('analytics.html',
        context={'request': request, 
                'model_predictions': show_model_table_initial,
                'reclass_conf_lev_cutoff': model_cutoff,
                'random_files_names': random_files_names,
                'concat_chart': concat_chart_json,
                'time_series_total': time_series_total_json,
                'time_series_class': time_series_class_json})


@router.post("/analytics_reclassify_predictions", response_class=HTMLResponse)
def form_post3(request: Request, conf_lev: float = Form(...)):
    pred_classes_new = filter_low_conf_images(conf_lev)
    model_predictions = {"image_ids": test_yolo_image_ids, 
            "confidence_scores": test_yolo_confs, 
            "predicted_classes_original": test_yolo_pred_classes, 
            "predicted_classes_new": pred_classes_new}

    df = pd.DataFrame.from_dict(model_predictions)
    df_export = df.copy()
    df_export.loc[df_export["predicted_classes_original"] == 1, "predicted_classes_original"] = "animal detected"
    df_export.loc[df_export["predicted_classes_original"] == 0, "predicted_classes_original"] = "animal not detected"
    df_export.loc[df_export["predicted_classes_new"] == 1, "predicted_classes_new"] = "animal detected"
    df_export.loc[df_export["predicted_classes_new"] == 0, "predicted_classes_new"] = "animal not detected"
    dfi.export(df_export,"static/images/analytics/data_frame/conf_table_reclassified.png")


    ## Class 0 ##
    file_names_class_0 = df[df.predicted_classes_new == 0][["image_ids"]].values.tolist()
 
    # Clear files in classification folders
    destination_folder = "static/images/analytics/predicted_0/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/analytics/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_0]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    ## Class 1 ##
    file_names_class_1 = df[df.predicted_classes_new == 1][["image_ids"]].values.tolist()

    # Clear files in classification folders
    destination_folder = "static/images/analytics/predicted_1/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/analytics/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_1]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    # save outputs
    _zip_files()
    
    # Get random images
    random_files_names = random_files()


    # creating Altair charts from model predictions
    conf_chart = make_conf_chart(df)
    class_chart = make_class_chart(df)
    time_series_total, time_series_class = time_series(df)
    time_series_total_json = time_series_total.to_json()
    time_series_class_json = time_series_class.to_json()
    
    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(y="shared")
    concat_chart_json = concat_chart.to_json()


    show_model_table_reclassified = True
    model_cutoff = float(conf_lev)

    return templates.TemplateResponse('analytics.html', 
        context={'request': request, 
                'model_predictions': show_model_table_reclassified,
                'reclass_conf_lev_cutoff': model_cutoff,
                'random_files_names': random_files_names,
                'concat_chart': concat_chart_json,
                'time_series_total': time_series_total_json,
                'time_series_class': time_series_class_json})


def random_files():
    # 3 random class 0
    random_file_0 = []
    i = 0
    while i < 15 :
        try:
            file_name = random_script.list_random_files('analytics/predicted_0/')
            if file_name not in random_file_0:
                random_file_0.append(file_name)
        except:
            random_file_0.append("not enough images in class")
        finally:
            i += 1
    random_file_0 = random_file_0 + ["not enough images in class"]*5
    random_file_0 = random_file_0[0:5]

    # 3 random class 1
    random_file_1 = []
    i = 0
    while i < 15 :
        try:
            file_name = random_script.list_random_files('analytics/predicted_1/')
            if file_name not in random_file_1:
                random_file_1.append(file_name)
        except:
            random_file_1.append("not enough images in class")
        finally:
            i += 1
    random_file_1 = random_file_1 + ["not enough images in class"]*5
    random_file_1 = random_file_1[0:5]
    
    random_file = [random_file_0, random_file_1]

    return random_file

def _clear_files(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def _copy_paste_files(list_of_file_paths_to_copy, destination_folder):
    for file in list_of_file_paths_to_copy: 
        shutil.copy(file, destination_folder)


def _zip_files():
    _clear_files("static/images/analytics/outputs/")
    for _class in ["predicted_0", "predicted_1"]:
        dst = "static/images/analytics/outputs/" + _class # where to save
        src = "static/images/analytics/" + _class + "/" # directory to be zipped
        shutil.make_archive(dst,'zip',src)

