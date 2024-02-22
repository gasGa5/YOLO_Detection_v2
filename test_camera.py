import cv2 
from ultralytics import YOLO
import datetime
import json
import pandas as pd
import requests
import pygame

class Camera_Detection():
    def __init__(self, weight_path, vedio_path = 0, conf_threshold = 0.6, frame_width = 640,
        frame_height = 480, frame = 30, wait_time = 1 , post_url = 'http://3.37.201.238/object-data-upload'):
        # pygame 초기화
        pygame.init()
        self.sound_file = "buzzer-message.mp3"
        self.sound = pygame.mixer.Sound(self.sound_file)
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
        self.cls_list = ["fire", "smoke", "cloud", "light", "etc"]
        self.frame = int(1000 / frame)
        self.wait_time = wait_time
        self.post_url = post_url
        self.start_time = 15
        self.end_time = 40
        
    def frame_set(self,):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_time * 1000)
        
    # def conf_condition(self, conf):
    #     if conf > self.conf_threshold:
    #         return True    
    #     else:
    #         return False
    
    def data_extract(self, object):        
        xmin, ymin, xmax, ymax = int(object[0]), int(object[1]), int(object[2]), int(object[3])
        conf = float(object[4])
        label = self.cls_list[int(object[5])]
        return xmin, ymin, xmax, ymax, label, conf   
     
    # def create_json(self, xmin, ymin, xmax, ymax, label, conf):
    #     data = {
    #     'label': label,
    #     'conf': conf,
    #     'box': [xmin, ymin, xmax, ymax]
    # }   
    #     json_data = json.dumps(data)   
         
    #     return json_data 
    
    def create_json(self, start, label, conf):
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        data = {
                "time": start,
                "label": label,
                "percentage": conf,
                }
        json_data = json.dumps(data)   
         
        return json_data 
    
    def post_data(self, json_data):
        response = requests.post(self.post_url, data=json_data, headers={"Content-Type": "application/json"})
        print(response.status_code)
        
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
            # print(f'time:{start}')
            success, frame = self.cap.read()
            
            if not success or self.cap.get(cv2.CAP_PROP_POS_MSEC) > self.end_time * 1000:
                break       
             
            if success:
                # if frame_skip == 0:
                    detection = self.model.predict(frame, imgsz = (self.frame_width,self.frame_height),
                                                   conf = self.conf_threshold)[0]          
                    # print(detection)
                    plot = detection.plot()
                    if self.detection_check(detection):
                        for objects in detection.boxes.data.tolist():
                            plot = detection.plot()
                            xmin, ymin, xmax, ymax, label, conf = self.data_extract(objects)
                            # print(label)
                            if label == 'fire':
                                self.sound.play()            
                            # json_data = self.create_json(xmin, ymin, xmax, ymax, label, conf)
                            # _, _, _, _, label, conf = self.data_extract(objects)                      
                            # json_data = self.create_json(start, label, conf)
                            # self.post_data(json_data)
                            # print(json_data)
                    # else:  
                        # plot = frame

                    # end = datetime.datetime.now()
                    # processing_time = (end - start).total_seconds()
                    # self.cal_fps(plot, start, end)
                    cv2.imshow('Detection', plot)

                    if self.stop_key('q'):
                        pygame.quit()
                        print('Stop Cam!')
                        break

                    # if processing_time > self.wait_time:  # 프레임 처리에 1초 이상 걸렸다면
                        # frame_skip = int(processing_time)  # 처리 시간에 따라 프레임을 건너뛰도록 설정
                # else:
                    # frame_skip -= 1  # 프레임을 건너뛰었다면, 건너뛸 프레임 수를 줄임
# 
            # else:
                # print('Cam error!')
                # break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    WEIGHT_PATH = './firesmoke3.pt'
    VEDIO_PATH = 'firevedio5.mp4'
    CONFIDENCE_THRESHOLD = 0.6
    FRAME_WIDTH = 1260
    FRAME_HEIGHT = 840
    FRAME = 60
    WAIT_TIME = 0.1
    POST_URL = 'http://3.37.201.238/object-data-upload'
    
    cam = Camera_Detection(weight_path = WEIGHT_PATH , vedio_path = VEDIO_PATH, 
                           conf_threshold = CONFIDENCE_THRESHOLD, 
                           frame_width = FRAME_WIDTH, frame_height = FRAME_HEIGHT 
                           , frame = FRAME, wait_time= WAIT_TIME, post_url = POST_URL)
    cam.frame_set()
    cam.Start_Detection()