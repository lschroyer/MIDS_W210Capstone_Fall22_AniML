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


def get_model_data():
    test_yolo_image_ids, test_yolo_pred_classes, test_yolo_bboxes, test_yolo_confs = parse_yolo_json("../data/filter_prediction/yolo_v5_prediction.json")
    model_predictions = {"image_ids": test_yolo_image_ids, 
                "confidence_scores": test_yolo_confs, 
                "predicted_classes_original": test_yolo_pred_classes}
    
    df = pd.DataFrame.from_dict(model_predictions)
    
    df.loc[(df["predicted_classes_original"] == "1") | 
                    (df["predicted_classes_original"] == 1), 
                    "predicted_classes_original"] = "animal_detected"
    df.loc[(df["predicted_classes_original"] == "0") | 
                    (df["predicted_classes_original"] == 0), 
                    "predicted_classes_original"] = "not_animal_detected"

    # shuffle data
    df = df.sample(frac=1)
    return df, False, df["predicted_classes_original"].unique().tolist()

# Initialize
df_global, already_reclassified, global_class_list = get_model_data()
df_global_reclassified = df_global.copy()
df_global_reclassified["predicted_classes_new"] = df_global_reclassified["predicted_classes_original"]


def filter_low_conf_images(df, conf_level):

    label = "animal_detected"

    # raise ValueError("break - testing")
    for index, image_id in enumerate(df["image_ids"]):
        if df["predicted_classes_original"][index] == label:
            if df["confidence_scores"][index] < conf_level:
                df["predicted_classes_new"][index] = "not_" + label
            else:
                df["predicted_classes_new"][index] = label
        else:
            df["predicted_classes_new"][index] = str(df["predicted_classes_new"][index])

    return df




@router.get("/review", response_class=HTMLResponse)
def form_get(request: Request):

    # Clear legacy outputs and create folders
    destination_folder = [
        "static/images/review/predicted_0/",
        "static/images/review/predicted_1/",
        "static/images/review/data_frame/",
        "static/images/review/outputs/"
    ]
    
    for folder in destination_folder:
        _clear_files(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)
    
    global df_global, global_class_list

    # Initialize data
    df_global, already_reclassified, global_class_list = get_model_data()

    df_global['predicted_classes_original'] = df_global.predicted_classes_original.replace(' ', '_', regex=True)
    dfi.export(df_global,"static/images/review/data_frame/conf_table_initial.png")



    ## Class 0 & 1 ##
    label_list = ["not_animal_detected", "animal_detected"]
    for j in [0, 1]:
        label_j = label_list[j]

        file_names_class_i = df_global[df_global.predicted_classes_original == label_j][["image_ids"]].values.tolist()
    
        # Clear files in classification folders
        destination_folder = "static/images/review/predicted_" + str(j) + "/"

        # Copy paste classified images:
        list_of_files_to_copy = ["static/images/review/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_i]

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


@router.post("/review_reclassify_predictions", response_class=HTMLResponse)
def form_post3(request: Request, conf_lev: float = Form(...)):
    global df_global_reclassified, already_reclassified

    # Clear legacy outputs for class of interest
    destination_folder = [
        "static/images/review/predicted_0",
        "static/images/review/predicted_1"
        ]

    for folder in destination_folder:
        _clear_files(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)

   
    df_global_reclassified = filter_low_conf_images(df_global_reclassified, conf_lev)
    
    already_reclassified = True

    dfi.export(df_global_reclassified, "static/images/review/data_frame/conf_table_reclassified.png")


    # Class 0 & 1#
    label_list = ["not_animal_detected", "animal_detected"]

    for j in [0, 1]:
        label_j = label_list[j]
        
        file_names_class_i = df_global_reclassified[df_global_reclassified.predicted_classes_new == label_j][["image_ids"]].values.tolist()
    
        # Clear files in classification folders
        destination_folder = "static/images/review/predicted_" + str(j) + "/"
        _clear_files(destination_folder)

        # Copy paste classified images:
        list_of_files_to_copy = ["static/images/review/inference_images/" + str(i[0] + ".jpg") for i in file_names_class_i]
        # logger.info(list_of_files_to_copy)
        _copy_paste_files(list_of_files_to_copy, destination_folder)

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


@router.get("/review_randomize", response_class=HTMLResponse)
def form_get2(request: Request):
    global df_global, df_global_reclassified, global_class_list    
    
    random_files_names = random_files()

    return templates.TemplateResponse('review.html', 
        context={'request': request, 
                # 'model_predictions': show_model_table_reclassified, 
                # 'reclass_conf_lev_cutoff': model_cutoff,
                'random_files_names': random_files_names
                })


def random_files():
    # 3 random class 0
    random_file_0 = []
    i = 0
    while i < 15 :
        try:
            file_name = random_script.list_random_files('review/predicted_0/')
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
            file_name = random_script.list_random_files('review/predicted_1/')
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
    _clear_files("static/images/review/outputs/")
    for _class in ["predicted_0", "predicted_1"]:
        dst = "static/images/review/outputs/" + _class # where to save
        src = "static/images/review/" + _class + "/" # directory to be zipped
        shutil.make_archive(dst,'zip',src)
