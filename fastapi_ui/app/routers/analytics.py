from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import json

import pandas as pd
import logging
import matplotlib.pyplot as plt
from pandas.plotting import table 
import dataframe_image as dfi



# setup loggers
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


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


@router.get("/analytics", response_class=HTMLResponse)
def form_get(request: Request):
    # logger.info("log test")
    logger.info(test_yolo_image_ids)
    model_predictions = {"image ids": test_yolo_image_ids, 
            "confidence scores": test_yolo_confs, 
            "predicted classes original": test_yolo_pred_classes}

    model_predictions_df = pd.DataFrame.from_dict(model_predictions)
    dfi.export(model_predictions_df,"static/images/analytics/conf_table_initial.png")


    show_model_table_initial = False
    return templates.TemplateResponse('analytics.html', context={'request': request, 'model_predictions': show_model_table_initial})


@router.post("/reclassify_predictions", response_class=HTMLResponse)
def form_post3(request: Request, conf_lev: float = Form(...)):
    pred_classes_new = filter_low_conf_images(conf_lev)
    model_predictions = {"image ids": test_yolo_image_ids, 
            "confidence scores": test_yolo_confs, 
            "predicted classes original": test_yolo_pred_classes, 
            "predicted classes new": pred_classes_new}

    model_predictions_df = pd.DataFrame.from_dict(model_predictions)

    dfi.export(model_predictions_df,"static/images/analytics/conf_table_reclassified.png")
    show_model_table_reclassified = True
    model_cutoff = float(conf_lev)

    return templates.TemplateResponse('analytics.html', 
        context={'request': request, 
                'model_predictions': show_model_table_reclassified, 
                'reclass_conf_lev_cutoff': model_cutoff})

