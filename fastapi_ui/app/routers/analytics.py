from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import altair as alt

import pandas as pd
import numpy as np
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

def make_class_chart(pred_df, width=450, height=300):
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


def make_conf_chart(pred_df, width=500, height=300):
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
        x = alt.X("confidence_scores:Q", bin=alt.Bin(maxbins=10), title="Confidence Level"),
        y = alt.Y("count():Q", title="Count"),
        color = alt.Color("predicted_classes_original:N", scale=alt.Scale(scheme="category10"), title = "Predicted Class"),
        tooltip = [alt.Tooltip("confidence_scores:Q", bin=alt.Bin(maxbins=10), title="Confidence Interval"),
                   alt.Tooltip("predicted_classes_original:N", title="Predicted Class"),
                   alt.Tooltip("count()", title="Count")],
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
    # creating time series from parsed dates
    try:
        # adding date as its own column
        pred_df["image_date"] = pd.to_datetime(dates, format="%m%d%Y")

        # grouping by date, imputing missing dates, and flattening dataframe for altair chart
        # this dataframe separates by predicted animal class
        date_df = pred_df.groupby(["image_date", "predicted_classes_original"]).size().unstack(fill_value=0).reset_index()
        date_df = date_df.set_index("image_date").asfreq("D", fill_value=0).reset_index()
        date_df_flat = pd.melt(date_df, id_vars=["image_date"])

        # further aggregating to calculate total animal counts, summing by predicted class
        date_df_total = date_df_flat.drop(["predicted_classes_original"], axis=1).groupby(["image_date"]).agg(["sum"])
        date_df_total.columns = date_df_total.columns.get_level_values(0)
        date_df_total.reset_index(inplace=True)

        # time-series chart for total detected animals in the dataset
        date_chart_total = alt.Chart(date_df_total).mark_line(point=True, strokeWidth=2).encode(
            x = alt.X("monthdate(image_date):T", title = "Image Date"),
            y = alt.Y("value:Q", title = "Count of Detected Animals"),
            tooltip = [alt.Tooltip("monthdate(image_date)", title = "Image Date"),
                       alt.Tooltip("value:Q", title = "Count of Detected Animals")]
        ).configure_point(
            size = 100
        ).properties(
            width = 900,
            height = 200,
            title = "Total Detected Animals Time Series"
        ).configure_axis(
            labelFontSize=20,
            titleFontSize=20
        ).configure_header(
            labelFontSize=20,
            titleFontSize=20
        ).configure_title(
            fontSize=20
        ).configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            labelFontSize=20,
            titleFontSize=15,
        )

        # defining title for center alignment
        date_chart_class_title = alt.TitleParams("Detected Animals Time Series by Animal Type", anchor="middle")
        # creating concatenated time-series charts for each animal class detected in the dataset
        date_chart_class = alt.Chart(date_df_flat, title=date_chart_class_title).mark_line(point=True, strokeWidth=2).encode(
            row = alt.Row("predicted_classes_original:N", title = "Predicted Animal Type"),
            x = alt.X("monthdate(image_date):T", title = "Image Date"),
            y = alt.Y("value:Q", title = "Detected Count"),
            color = alt.Color("predicted_classes_original:N", scale=alt.Scale(scheme="category10"), title="Predicted Animal Type"),
            tooltip = [alt.Tooltip("monthdate(image_date)", title = "Image Date"),
                       alt.Tooltip("predicted_classes_original", title = "Animal Type"),
                       alt.Tooltip("value", title = "Detected Count")]
        ).configure_point(
            size = 100
        ).properties(
            width = 900,
            height = 200,
            # title = Detected Animals Time Series by Animal Type
        ).configure_axis(
            labelFontSize=20,
            titleFontSize=20
        ).configure_header(
            labelFontSize=20,
            titleFontSize=20
        ).configure_title(
            fontSize=20,

        ).configure_legend(
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            labelFontSize=20,
            titleFontSize=15,
        )
    
    # if the dates in image names cannot be parsed, return None for time series charts
    except ValueError:
        date_chart_total = None
        date_chart_class = None
    
    return date_chart_total, date_chart_class

def get_model_data():
    test_yolo_image_ids, test_yolo_pred_classes, test_yolo_bboxes, test_yolo_confs = parse_yolo_json("../data/classification_prediction/yolo_v5_prediction.json")
    model_predictions = {"image_ids": test_yolo_image_ids, 
                "confidence_scores": test_yolo_confs, 
                "predicted_classes_original": test_yolo_pred_classes}
    
    df = pd.DataFrame.from_dict(model_predictions)
    
    # df.loc[(df["predicted_classes_original"] == "1") | 
    #                 (df["predicted_classes_original"] == 1), 
    #                 "predicted_classes_original"] = "animal_detected"
    df.loc[(df["predicted_classes_original"] == "0") | 
                    (df["predicted_classes_original"] == 0), 
                    "predicted_classes_original"] = "unknown_classification"

    df['predicted_classes_original'] = df.predicted_classes_original.replace(' ', '_', regex=True)

    # shuffle data
    df = df.sample(frac=1)

    # get initial conf table
    label_list = df["predicted_classes_original"].unique()
    
    df_classification_cuttoffs_initial = pd.DataFrame(
        {"class_name": label_list, 
        "confidence_cutoff": ["default"] * len(label_list)}
        )

    # get class counts
    df_class_counts_initial = df['predicted_classes_original'].value_counts().to_frame().rename(columns={"predicted_classes_original": "count"})

    return df, False, df["predicted_classes_original"].unique().tolist(), df_classification_cuttoffs_initial, df_class_counts_initial

# Initialize for global variables
df_global, already_reclassified, global_class_list, df_classification_cuttoffs, df_class_counts = get_model_data()
df_global_reclassified = df_global.copy()
df_global_reclassified["predicted_classes_new"] = df_global_reclassified["predicted_classes_original"]

def filter_low_conf_images(df, conf_level, label = None):
    
    if already_reclassified == False:
        df["predicted_classes_new"] = df["predicted_classes_original"]
        label_list = df["predicted_classes_original"].unique()
    else:
        label_list = df["predicted_classes_new"].unique()

    # raise ValueError("break - testing")
    if label not in label_list or label is not None:
        for index, image_id in enumerate(df["image_ids"]):
            if df["predicted_classes_original"][index] == label:
                if df["confidence_scores"][index] < conf_level:
                    df["predicted_classes_new"][index] = "not_" + label
                else:
                    df["predicted_classes_new"][index] = label
            else:
                df["predicted_classes_new"][index] = str(df["predicted_classes_new"][index])
    else:
        raise ValueError("need correct class or 'all'")
    return df

@router.get("/analytics", response_class=HTMLResponse)
def form_get(request: Request):
    global df_global, global_class_list, df_classification_cuttoffs, df_class_counts

    # Initialize data
    df_global, already_reclassified, global_class_list, df_classification_cuttoffs, df_class_counts = get_model_data()

    # Clear legacy outputs and create folders
    destination_folder = [
        "static/images/analytics/predicted_classes/",
        "static/images/analytics/data_frame/",
        "static/images/analytics/outputs/"
    ]
    
    for folder in destination_folder:
        _clear_files(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)


    dfi.export(df_global,"static/images/analytics/data_frame/conf_table_initial.png")
    dfi.export(df_classification_cuttoffs.style.hide_index(), 
        "static/images/analytics/data_frame/cutoff_levels_table_initial.png")
    dfi.export(df_class_counts,
        "static/images/analytics/data_frame/class_counts_initial.png")


    # ToDo - if time allows, change pandas table to html
    # with open('static/images/analytics/data_frame/conf_table_initial.html', 'w') as fo:
    #     df_global.to_html(fo)

    # Zip all classes and get random files for all classes
    _zip_files(class_name = "all_classes", specific_class = False)
    random_files_names = {"all_classes": random_files_i(predicted_path="analytics/inference_images/")}

    # Random files and outputs workflow
    random_file_workflow(df_global)


    # creating Altair charts from model predictions
    df_global_copy = df_global.copy()
    conf_chart = make_conf_chart(df_global_copy)
    class_chart = make_class_chart(df_global_copy)
    time_series_total, time_series_class = time_series(df_global_copy)
    # if the function returns None for the time series, create empty dict/JSON
    time_series_total_json = time_series_total.to_json() if time_series_total else None
    time_series_class_json = time_series_class.to_json() if time_series_class else None
    
    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(
        y="shared"
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).configure_header(
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        fontSize=20
    ).configure_legend(
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=15,
    )
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
                'time_series_class': time_series_class_json,
                'class_name': "all_classes",
                "class_list": global_class_list})


@router.post("/analytics_reclassify_predictions", response_class=HTMLResponse)
def form_post(request: Request, conf_lev: float = Form(...), pred_class: str = Form(...)):
    global df_global_reclassified, already_reclassified, df_classification_cuttoffs

    # Clear legacy outputs for class of interest
    destination_folder = [
        "static/images/analytics/predicted_classes/predicted_" + pred_class,
        "static/images/analytics/predicted_classes/predicted_not_" + pred_class,
         "static/images/analytics/data_frame/"
         ]

    for folder in destination_folder:
        if not os.path.exists(folder):
            os.mkdir(folder)
        _clear_files(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)

    if already_reclassified == False:
        df_global_reclassified = filter_low_conf_images(df_global, conf_lev, pred_class)   
    else:
        df_global_reclassified = filter_low_conf_images(df_global_reclassified, conf_lev, pred_class)
    already_reclassified = True

    df_classification_cuttoffs.loc[(df_classification_cuttoffs.class_name ==  pred_class),["confidence_cutoff"]] = conf_lev

    df_class_counts = df_global_reclassified.groupby(
        ['predicted_classes_original','predicted_classes_new']
        ).size().to_frame()
    df_class_counts.index = df_class_counts.index.set_names(['predicted_classes_original', 'predicted_classes_new'])
    df_class_counts = df_class_counts.reset_index()

    dfi.export(df_global_reclassified,"static/images/analytics/data_frame/conf_table_reclassified.png")
    dfi.export(df_classification_cuttoffs.style.hide_index(), 
        "static/images/analytics/data_frame/cutoff_levels_table_reclassified.png")
    dfi.export(df_class_counts.style.hide_index(),
        "static/images/analytics/data_frame/class_counts_reclassified.png")



    # Random files and outputs workflow
    random_files_names = random_file_workflow(df_global_reclassified)

    # creating Altair charts from model predictions
    df_global_reclassified_copy = df_global_reclassified.copy()
    conf_chart = make_conf_chart(df_global_reclassified_copy)
    class_chart = make_class_chart(df_global_reclassified_copy)
    time_series_total, time_series_class = time_series(df_global_reclassified_copy)
    time_series_total_json = time_series_total.to_json() if time_series_total else None
    time_series_class_json = time_series_class.to_json() if time_series_total else None
    
    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(
        y="shared"
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).configure_header(
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        fontSize=20
    ).configure_legend(
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=15,
    )
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
                'time_series_class': time_series_class_json,
                'class_name': pred_class,
                "class_list": global_class_list})


@router.post("/analytics_randomize_images", response_class=HTMLResponse)
async def form_post2(request: Request, random_class_name: str = Form(...)):
    global df_global, df_global_reclassified, global_class_list
    
    random_class_name = random_class_name.lower()
    random_class_name = random_class_name.replace(' ', '_')
    random_class_name = random_class_name.replace('"', '')
    random_class_name = random_class_name.replace("'", '')

    df_filtered = df_global_reclassified[
        (df_global_reclassified.predicted_classes_new == random_class_name) |
        (df_global_reclassified.predicted_classes_new == "not_" + random_class_name)]

    if random_class_name == "all_classes":
        random_files_names = {}
        random_files_names["all_classes"] = random_files_i(predicted_path="analytics/inference_images/")
    else:
        random_files_names = random_file_workflow(df_filtered)



    # creating Altair charts from model predictions
    df_global_copy = df_global.copy()
    conf_chart = make_conf_chart(df_global_copy)
    class_chart = make_class_chart(df_global_copy)
    time_series_total, time_series_class = time_series(df_global_copy)
    time_series_total_json = time_series_total.to_json()
    time_series_class_json = time_series_class.to_json()

    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(y="shared")
    concat_chart_json = concat_chart.to_json()
    
    return templates.TemplateResponse('analytics.html',
        context={'request': request, 
                'random_files_names': random_files_names,
                'concat_chart': concat_chart_json,
                'time_series_total': time_series_total_json,
                'time_series_class': time_series_class_json,
                'class_name': random_class_name,
                "class_list": global_class_list})

@router.post("/analytics_reclassify_image", response_class=HTMLResponse)
def form_post2(request: Request, img_name: str = Form(...), new_class: str = Form(...)):
    global df_global, df_global_reclassified, global_class_list

    new_class = new_class.lower()
    new_class = new_class.replace(' ', '_')
    new_class = new_class.replace('"', '')
    new_class = new_class.replace("'", '')
    img_name_no_suffix = img_name.replace('.jpg', '')

    # Reclassify Individual image
    df_global_reclassified.loc[(
        df_global_reclassified["image_ids"] == img_name_no_suffix), 
                    "predicted_classes_new"] = new_class

    df_class_counts = df_global_reclassified.groupby(
        ['predicted_classes_original','predicted_classes_new']
        ).size().to_frame()
    df_class_counts.index = df_class_counts.index.set_names(['predicted_classes_original', 'predicted_classes_new'])
    df_class_counts = df_class_counts.reset_index()


    # Get standard UI outputs
    dfi.export(df_global_reclassified,"static/images/analytics/data_frame/conf_table_reclassified.png")
    dfi.export(df_class_counts.style.hide_index(),
        "static/images/analytics/data_frame/class_counts_reclassified.png")
    
    df_filtered = df_global_reclassified[
        (df_global_reclassified.predicted_classes_new == new_class) |
        (df_global_reclassified.predicted_classes_new == "not_" + new_class)]

    if new_class == "all_classes":
        random_files_names = {}
        random_files_names["all_classes"] = random_files_i(predicted_path="analytics/inference_images/")
    else:
        random_files_names = random_file_workflow(df_filtered)

    # creating Altair charts from model predictions
    df_global_copy = df_global.copy()
    conf_chart = make_conf_chart(df_global_copy)
    class_chart = make_class_chart(df_global_copy)
    time_series_total, time_series_class = time_series(df_global_copy)
    time_series_total_json = time_series_total.to_json()
    time_series_class_json = time_series_class.to_json()

    # concatenating charts horizontally and saving as a JSON object to easily parse with JavaScript on the frontend
    concat_chart = (class_chart | conf_chart).resolve_scale(y="shared")
    concat_chart_json = concat_chart.to_json()

    show_model_table_reclassified = True


    return templates.TemplateResponse('analytics.html',
        context={'request': request, 
                'random_files_names': random_files_names,
                'model_predictions': show_model_table_reclassified,
                'concat_chart': concat_chart_json,
                'time_series_total': time_series_total_json,
                'time_series_class': time_series_class_json,
                'class_name': new_class,
                "class_list": global_class_list})


# @app.route('/pass_val',methods=['POST'])
# def pass_val():
#     name=request.args.get('value')
#     print('name',name)
#     return jsonify({'reply':'success'})


def random_file_workflow(df):
    global global_class_list
    random_file_names = {}
    
    if "predicted_classes_new" in df.columns:
        class_list = np.concatenate(
            (df["predicted_classes_original"].unique(),
            df["predicted_classes_new"].unique()),
            axis=None).tolist()
    else:
        class_list = df["predicted_classes_original"].unique().tolist()

    class_list.extend(x for x in global_class_list if x not in class_list)
    class_list = list(set(class_list))

    logger.info("-------------")
    logger.info(class_list)

    for class_name in class_list:
        if "not_" + class_name.replace('not_', '') not in class_list:
            class_list = np.append(class_list, ["not_" + class_name])

    # Loop over all classes and 'not' classes
    for class_name in class_list:
        logger.info("************")
        logger.info(class_name)
        # Create files
        dst = "static/images/analytics/predicted_classes/predicted_" + class_name 
        if not os.path.exists(dst):
            os.mkdir(dst)

        ## Class I ##
        if "predicted_classes_new" in df.columns:
            file_names_class_i = df[df.predicted_classes_new == class_name][["image_ids"]].values.tolist()
        else:
            file_names_class_i = df[df.predicted_classes_original == class_name][["image_ids"]].values.tolist()
    
        # Clear files in classification folders
        destination_folder = "static/images/analytics/predicted_classes/predicted_" + class_name + "/"
        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)
        _clear_files(destination_folder)

        list_of_files_to_copy = []
        for files_list in file_names_class_i: #list in list, grab first element
            files = files_list[0]

            # handle empy directory
            if len(files) > 0:
                list_of_files_to_copy.append("static/images/analytics/inference_images/" + str(files + ".jpg"))
        _copy_paste_files(list_of_files_to_copy, destination_folder)

        # save outputs
        _zip_files(class_name)
        
        # Get random images
        random_file_names[class_name] = random_files_i(class_name)
    
    return random_file_names


def random_files_i(class_name: str = "", predicted_path = 'analytics/predicted_classes/predicted_'):
    # 5 random class i
    random_file = []
    i = 0
    while i < 15 :
        try:
            if class_name == "":
                file_name = random_script.list_random_files("analytics/inference_images/")
            else:
                file_name = random_script.list_random_files(predicted_path + class_name + '/')
            
            if file_name not in random_file:
                random_file.append(file_name)
        except:
            random_file.append("not enough images in class")
        finally:
            i += 1
    random_file = random_file + ["not enough images in class"]*30

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


def _zip_files(class_name, specific_class = True):
    if specific_class:
        dst = "static/images/analytics/outputs/" + class_name # where to save
        src = "static/images/analytics/predicted_classes/predicted_" + class_name + "/" # directory to be zipped
        shutil.make_archive(dst,'zip',src)
    else:
        dst = "static/images/analytics/outputs/all_classes" # where to save
        src = "static/images/analytics/inference_images/" # directory to be zipped
        shutil.make_archive(dst,'zip',src)
        
    

