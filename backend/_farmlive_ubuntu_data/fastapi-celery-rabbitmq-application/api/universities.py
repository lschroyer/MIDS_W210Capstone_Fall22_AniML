import json

import httpx

from schemas.schemas import University

# Ivan add import time.
import time

# Ivan add import yolov5.
import yolov5

# Ivan add import os.
import os


url = 'http://universities.hipolabs.com/search'


def get_all_universities_for_country(country: str) -> dict:
    print('get_all_universities_for_country ', country)
    params = {'country': country}
    client = httpx.Client()
    response = client.get(url, params=params)
    response_json = json.loads(response.text)
    universities = []
    for university in response_json:
        university_obj = University.parse_obj(university)
        universities.append(university_obj)
    return {country: universities}

# Ivan: create run_tranining function to run the training job
def run_training(job: str):
    from yolov5 import train, val, detect, export
    print ("job: ", job)
    print ("type of job: ", type(job))
    job_number="job1"

    # train.run(imgsz=640, data='coco128.yaml')
    # val.run(imgsz=640, data='coco128.yaml', weights='yolov5s.pt')
    # results=train.run(imgsz=640, data='data.yaml', epochs=3, batch_size=16, weights='yolov5s.pt')
    
    # Ivan (11/6/22): Change parameter to train Lana's AmiML dataset
    # Ivan (12/5/22): Turn-Off: Change parameter to train Lana's AmiML dataset
    # results=train.run(imgsz=640, data='data.yaml', epochs=150, batch_size=16, weights='yolov5l.pt')

    # Ivan (11/6/22): Change to 10 epochs for quick test
    # Ivan (12/5/22): Turn-On: Change to 10 epochs for quick test
    results=train.run(imgsz=640, data='data.yaml', epochs=10, batch_size=16, weights='yolov5l.pt')


    # val.run(imgsz=640, data='data.yaml', weights='yolov5s.pt')
    # detect.run(imgsz=640)
    # export.run(imgsz=640, weights='yolov5s.pt')

    print ("results: ", results)
    print ("type of results: ", type(results))

    # return job_number
    return results


