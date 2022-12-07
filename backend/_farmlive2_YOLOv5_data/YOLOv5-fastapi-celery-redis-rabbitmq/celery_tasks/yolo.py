import logging
import torch
import matplotlib.pyplot as plt


class YoloModel:
    def __init__(self):        
        ######## Ivan (11/5/22): Original default YOLOv5x
        # self.model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True) 

        ######## Ivan (11/5/22): Change to load Lana's custom trained 'best_sample150l.pt' model from local
        # Ivan (11/5/22): SUCESS Option (1) to use local source './yolov5'   
        # self.model = torch.hub.load('./yolov5', 'custom', path='./model/best_sample150l.pt', source='local', force_reload=True) 
        # Ivan (11/5/22): SUCESS Option (2) to use the torch.hub 'ultralytics/yolov5' instead of local source.
        # self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./api/model/best_sample150l.pt', force_reload=True) 
        
        ######## Ivan (11/6/22): Testing with Ivan's custom trained model 'ivan_api_trained_best.pt' from local
        # Ivan (11/6/22): SUCESS Option (1) to use local source './yolov5'   
        # self.model = torch.hub.load('./yolov5', 'custom', path='./model/ivan_api_trained_best.pt', source='local', force_reload=True)

        # Ivan (11/6/22): SUCESS Option (2) to use the torch.hub 'ultralytics/yolov5' instead of local source.
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./api/model/ivan_api_trained_best.pt', force_reload=True)

        self.model.eval()

    def predict(self, img):
        # Ivan added print
        print ("task.py model.predict = ", "I am here.")
        try:
            with torch.no_grad():
                result = self.model(img)
            # Ivan added print
            print ("model results = ", result)
            print ("type model results = ", type(result))

            # result.save('api/static/results/')
            # Ivan: Use the save_dir parameter
            # save_dir = increment_path(save_dir, exist_ok=save_dir != 'runs/detect/exp', mkdir=True)  # increment save_dir
            result.save(save_dir='api/static/results/', exist_ok=True ) 

            final_result = {}
            data = []

            file_name = f'static/{result.files[0]}'

            # Ivan added print
            print ("file_name = ", file_name)
            print ("result.xywhn[0] = ", result.xywhn[0])
            print ("len(result.xywhn[0]) = ", len(result.xywhn[0]))

            for i in range(len(result.xywhn[0])):
                # Ivan: try to get away from the CPU error.  
                # x, y, w, h, prob, cls = result.xywhn[0][i].numpy()
                x, y, w, h, prob, cls = result.xywhn[0][i].cpu().numpy()
                preds = {}
                preds['x'] = str(x)
                preds['y'] = str(y)
                preds['w'] = str(w)
                preds['h'] = str(h)
                preds['prob'] = str(prob)
                preds['class'] = result.names[int(cls)]
                data.append(preds)

            return {'file_name': file_name, 'bbox': data}
        except Exception as ex:
            logging.error(str(ex))
            return None
