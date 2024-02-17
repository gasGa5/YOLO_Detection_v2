import cv2 
from ultralytics import YOLO
import datetime
import json
import pandas as pd

class Camera_Detection():
    def __init__(self, weight_path, vedio_path = 0, conf_threshold = 0.6, frame_width = 640,
        frame_height = 480):
        
        self.weight_path = weight_path
        self.vedio_path = vedio_path
        self.model = YOLO(self.weight_path)
        self.cap = cv2.VideoCapture(vedio_path)
        self.conf_threshold = conf_threshold
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cls_list = ["fire", "person"]
        
    def frame_set(self,):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
    
    def conf_condition(self, data):
        conf = float(data[4])
        if conf > self.conf_threshold:
            return True
        
        else:
            return False
    
    # def data_extract(self, detection):
    #     for data in detection.boxes.data.tolist():
    #         print(data)
    #         if self.conf_condition(data):
    #             xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    #             conf = float(data[4])
    #             label = int(data[5])
    #             return xmin, ymin, xmax, ymax, label, conf                
     
    def create_json(self, objects):
        data = {
        'label': objects['name'].tolist(),
        'conf': objects['confidence'].tolist(),
        'box': objects['box'].tolist()
    }   
        json_data = json.dumps(data)   
         
        return json_data 
                    
    # def render(self, frame, xmin, ymin, xmax, ymax, label, conf):
        # cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.green, 2)
        # cv2.putText(frame, self.cls_list[label]+' '+str(round(conf, 2))+'%', (xmin, ymin), cv2.FONT_ITALIC, 1, self.black , 2)
    
    def cal_fps(self, frame, start, end):
        total = (end - start).total_seconds()
        print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')
        fps = f'FPS: {1 / total:.2f}'
        cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.imshow('frame', frame)
        
    def stop_key(self,key):
        if cv2.waitKey(1) & 0xff == ord(key):
            return True
    
    def detection_check(self, detection) -> bool:
        if detection.boxes.cls.shape[0] != 0:
            return True
        else:
            return False     
    
    def Output_extract(self, detection):
        json_data = detection.tojson()
        objects = pd.read_json(json_data)
        objects = objects.reset_index(drop=True)
        return objects

    def Start_Detection(self,):
        while self.cap.isOpened():
            start = datetime.datetime.now()
            success, frame = self.cap.read()        
            if success:
                detection = self.model(frame)[0]
                plot = detection.plot()
                if self.detection_check(detection) is True:
                    objects = self.Output_extract(detection)
                    # print(objects)
                    # xmin, ymin, xmax, ymax, label, conf = self.data_extract(detection)
                    # print(label)
                    # self.render(frame, xmin, ymin, xmax, ymax, label, conf)
                    json_data = self.create_json(objects)
                    print(json_data)
                end = datetime.datetime.now()
                self.cal_fps(plot, start, end)
                cv2.imshow('Detection', plot)
        
                if self.stop_key('q'):
                    print('Stop Cam!')
                    break
                            
            else:
                print('Cam error!')
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    WEIGHT_PATH = './firesmoke.pt'
    VEDIO_PATH = '창밖으로 치솟는 시뻘건 불길 화성 고층 오피스텔 화재  제보영상  SBS.mp4'
    CONFIDENCE_THRESHOLD = 0.6
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    cam = Camera_Detection(WEIGHT_PATH , VEDIO_PATH, CONFIDENCE_THRESHOLD, FRAME_WIDTH, FRAME_HEIGHT)
    cam.frame_set()
    cam.Start_Detection()