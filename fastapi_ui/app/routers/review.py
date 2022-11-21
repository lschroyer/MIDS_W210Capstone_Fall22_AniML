from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

import pandas as pd
import logging
# import matplotlib.pyplot as plt
import dataframe_image as dfi

import sys
sys.path.append("..") # Adds higher directory to python modules path.


from static import random_script
import os, shutil


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

test_yolo_image_ids, test_yolo_pred_classes, test_yolo_bboxes, test_yolo_confs = parse_yolo_json("../data/yolo_v5_prediction.json")
test_yolo_pred_classes_new = test_yolo_pred_classes.copy()

def filter_low_conf_images(conf_level):
    for index, image_id in enumerate(test_yolo_image_ids):
        if test_yolo_confs[index] < conf_level:
            test_yolo_pred_classes_new[index] = 0
        else:
            test_yolo_pred_classes_new[index] = 1
    return test_yolo_pred_classes_new

@router.get("/review", response_class=HTMLResponse)
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
    dfi.export(df_export,"static/images/analytics/conf_table_initial.png")
    

    ## Class 0 ##
    file_names_class_0 = df[df.predicted_classes_original == 0][["image_ids"]].values.tolist()
    # for col in model_predictions_df.columns:
    #     logger.info(col)
    # logger.info(file_names_class_0)

    # Clear files in classification folders
    destination_folder = "static/images/predicted_0/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_0]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    ## Class 1 ##
    file_names_class_1 = df[df.predicted_classes_original == 1][["image_ids"]].values.tolist()

    # Clear files in classification folders
    destination_folder = "static/images/predicted_1/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_1]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    # save outputs
    _zip_files()

    # Get random images
    random_files_names = random_files()

    model_cutoff = "default model prediction"
    show_model_table_initial = False
    return templates.TemplateResponse('review.html', 
            context={'request': request, 
                    'model_predictions': show_model_table_initial,
                    'reclass_conf_lev_cutoff': model_cutoff,
                    'random_files_names': random_files_names
                    })


@router.post("/reclassify_predictions", response_class=HTMLResponse)
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
    dfi.export(df_export,"static/images/analytics/conf_table_reclassified.png")


    ## Class 0 ##
    file_names_class_0 = df[df.predicted_classes_new == 0][["image_ids"]].values.tolist()
 
    # Clear files in classification folders
    destination_folder = "static/images/predicted_0/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_0]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    ## Class 1 ##
    file_names_class_1 = df[df.predicted_classes_new == 1][["image_ids"]].values.tolist()

    # Clear files in classification folders
    destination_folder = "static/images/predicted_1/"
    _clear_files(destination_folder)

    # Copy paste classified images:
    list_of_files_to_copy = ["static/images/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_1]
    # logger.info(list_of_files_to_copy)
    _copy_paste_files(list_of_files_to_copy, destination_folder)

    # save outputs
    _zip_files()
    
    # Get random images
    random_files_names = random_files()

    show_model_table_reclassified = True
    model_cutoff = float(conf_lev)

    return templates.TemplateResponse('review.html', 
        context={'request': request, 
                'model_predictions': show_model_table_reclassified, 
                'reclass_conf_lev_cutoff': model_cutoff,
                'random_files_names': random_files_names
                })

def random_files():
    # 3 random class 0
    random_file_0 = []
    i = 0
    while i < 15 :
        try:
            file_name = random_script.list_random_files('predicted_0/')
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
            file_name = random_script.list_random_files('predicted_1/')
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
    _clear_files("static/images/outputs/")
    for _class in ["predicted_0", "predicted_1"]:
        dst = "static/images/outputs/" + _class # where to save
        src = "static/images/" + _class + "/" # directory to be zipped
        shutil.make_archive(dst,'zip',src)
