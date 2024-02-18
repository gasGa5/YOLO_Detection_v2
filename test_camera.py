import cv2 
from ultralytics import YOLO
import datetime
import json
import pandas as pd

class Camera_Detection():
    def __init__(self, weight_path, vedio_path = 0, conf_threshold = 0.6, frame_width = 640,
        frame_height = 480, frame = 30, wait_time = 1):
        
        self.weight_path = weight_path
        self.vedio_path = vedio_path
        self.model = YOLO(self.weight_path)
        self.cap = cv2.VideoCapture(vedio_path)
        self.conf_threshold = conf_threshold
        # self.green = (0, 255, 0)
        # self.black = (0, 0, 0)
        self.frame_width = frame_width
        self.frame_height = frame_height
        # self.cls_list = ["fire", "person"]
        self.frame = int(1000 / frame)
        self.wait_time = wait_time
        
    def frame_set(self,):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
    
    # def conf_condition(self, conf):
    #     if conf > self.conf_threshold:
    #         return True    
    #     else:
    #         return False
    
    def data_extract(self, object):        
        xmin, ymin, xmax, ymax = int(object[0]), int(object[1]), int(object[2]), int(object[3])
        conf = float(object[4])
        label = int(object[5])
        return xmin, ymin, xmax, ymax, label, conf   
     
    def create_json(self, xmin, ymin, xmax, ymax, label, conf):
        data = {
        'label': label,
        'conf': conf,
        'box': [xmin, ymin, xmax, ymax]
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
        if cv2.waitKey(self.frame) & 0xff == ord(key):
            return True
    
    def detection_check(self, detection) -> bool:
        if detection.boxes.conf.numel() > 0:
            return True
        else:
            return False     
    
    def Output_extract(self, detection):
        json_data = detection.tojson()
        objects = pd.read_json(json_data)
        objects = objects.reset_index(drop=True)
        return objects

    def Start_Detection(self,):
        frame_skip = 0
        while self.cap.isOpened():
            start = datetime.datetime.now()
            success, frame = self.cap.read()        
            if success:
                if frame_skip == 0:
                    detection = self.model.predict(frame, imgsz = (self.frame_width,self.frame_height),
                                                   conf = self.conf_threshold)[0]           
                    if self.detection_check(detection):
                        for objects in detection.boxes.data.tolist():
                            plot = detection.plot()
                            xmin, ymin, xmax, ymax, label, conf = self.data_extract(objects)                      
                            json_data = self.create_json(xmin, ymin, xmax, ymax, label, conf)
                            print(json_data)
                    else:  
                        plot = frame

                    end = datetime.datetime.now()
                    processing_time = (end - start).total_seconds()
                    self.cal_fps(plot, start, end)
                    cv2.imshow('Detection', plot)

                    if self.stop_key('q'):
                        print('Stop Cam!')
                        break

                    if processing_time > self.wait_time:  # 프레임 처리에 1초 이상 걸렸다면
                        frame_skip = int(processing_time)  # 처리 시간에 따라 프레임을 건너뛰도록 설정
                else:
                    frame_skip -= 1  # 프레임을 건너뛰었다면, 건너뛸 프레임 수를 줄임

            else:
                print('Cam error!')
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    WEIGHT_PATH = './firesmoke.pt'
    VEDIO_PATH = 'gangreng_fire.mp4'
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_WIDTH = 160
    FRAME_HEIGHT = 256
    FRAME = 30
    WAIT_TIME = 1
    
    cam = Camera_Detection(weight_path = WEIGHT_PATH , vedio_path = VEDIO_PATH, 
                           conf_threshold = CONFIDENCE_THRESHOLD, 
                           frame_width = FRAME_WIDTH, frame_height = FRAME_HEIGHT 
                           , frame = FRAME, wait_time= WAIT_TIME)
    cam.frame_set()
    cam.Start_Detection()