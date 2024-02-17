import cv2 
from ultralytics import YOLO
import datetime
import json

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
    
    def data_extract(self, detection):
        for data in detection.boxes.data.tolist():
            if self.conf_condition(data):
                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                label = int(data[5])
                conf = float(data[4])
                
                return xmin, ymin, xmax, ymax, label, conf
     
    def create_json(self, xmin, ymin, xmax, ymax, label, conf):
        data = {
        'label': label,
        'conf': conf,
        'box': [xmin, ymin, xmax, ymax]
    }        
        json_data = json.dumps(data)    
        return json_data 
                    
    def render(self, frame, xmin, ymin, xmax, ymax, label, conf):
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.green, 2)
        cv2.putText(frame, self.cls_list[label]+' '+str(round(conf, 2))+'%', (xmin, ymin), cv2.FONT_ITALIC, 1, self.black , 2)
    
    def cal_fps(self, frame, start, end):
        total = (end - start).total_seconds()
        print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')
        fps = f'FPS: {1 / total:.2f}'
        cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('frame', frame)
        
    def stop_key(self,key):
        if cv2.waitKey(1) & 0xff == ord(key):
            return True
    
    def Start_Detection(self,):
        while True:
            start = datetime.datetime.now()
            success, frame = self.cap.read()
            
            if success:
                detection = self.model(frame)[0]
                xmin, ymin, xmax, ymax, label, conf = self.data_extract(detection)
                self.render(frame, xmin, ymin, xmax, ymax, label, conf)
                json_data = self.create_json(xmin, ymin, xmax, ymax, label, conf)
                print(json_data)
                end = datetime.datetime.now()
                self.cal_fps(frame, start, end)
                # annotated_frame = results.render()[0]
                # cv2.imshow('Detection', annotated_frame)
        
                if self.stop_key('q'):
                    print('Stop Cam!')
                    break
                            
            else:
                print('Cam error!')
                break
            
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    WEIGHT_PATH = './runs/detect/train40/weights/best.pt'
    VEDIO_PATH = 0
    CONFIDENCE_THRESHOLD = 0.6
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    cam = Camera_Detection(WEIGHT_PATH , VEDIO_PATH, CONFIDENCE_THRESHOLD, FRAME_WIDTH, FRAME_HEIGHT)
    cam.frame_set()
    cam.Start_Detection()