from ultralytics import YOLO
import cv2
import json
import datetime
import socket
import requests
import pygame
import torch

class TCP_stream():
    def __init__(self, tcp_path, model_path, frame_width, frame_height, framerate, conf_thre, frame, host, port, post_url = 'http://3.37.201.238/object-data-upload') -> None:
        self.tcp_path = tcp_path
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # CUDA 디바이스 설정
        self.model = YOLO(model_path).to(self.device)  # 모델을 CUDA 디바이스로 이동
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.framerate = framerate
        self.conf_thre = conf_thre
        self.frame = frame
        self.host = host
        self.port = port 
        self.post_url = post_url
        self.cls_list = ["fire", "smoke", "cloud", "light", "etc"]
        pygame.init()
        self.sound_file = "buzzer-message.mp3"
        self.sound = pygame.mixer.Sound(self.sound_file)
        
    def client_socket(self,):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        while True:
            key = input('start detected your input "q": ')
            payload = json.dumps({'key': key,
                       'width': self.frame_width,
                       'height': self.frame_height,
                       'framerate': self.framerate
                       })
            
            s.sendall(payload.encode())
           
            data = s.recv(1024)
            if data.decode() == 'TCP_Server started.':
                print('server_data:', data.decode())
                s.close()
                break

    def stream(self,):
        self.client_socket()
        
        results = self.model.predict(self.tcp_path, imgsz = (self.frame_height,self.frame_width),
                                                   conf = self.conf_thre, stream=True,)
        
        while True:
            for detection in results:
                plot = detection.plot()
                if self.detection_check(detection):
                    for objects in detection.boxes.data.tolist():
                        _, _, _, _, label, conf = self.data_extract(objects)                      
                        # json_data = self.create_json(label, conf)
                        # self.post_data(json_data)
                        if label == 'fire':
                                self.sound.play()
                          
                cv2.imshow('Object Detection', plot)
                       
            if self.stop_key('q'):
                pygame.quit()
                break

        cv2.destroyAllWindows()
    
    def detection_check(self, detection) -> bool:
        if detection.boxes.conf.numel() > 0:
            return True
        else:
            return False
        
    def data_extract(self, object):        
        xmin, ymin, xmax, ymax = int(object[0]), int(object[1]), int(object[2]), int(object[3])
        conf = float(object[4])
        label = self.cls_list[int(object[5])]
        return xmin, ymin, xmax, ymax, label, conf
    
    def stop_key(self,key):
        if cv2.waitKey(self.frame) & 0xff == ord(key):
            return True
    
    def cal_fps(self, frame, start, end):
        total = (end - start).total_seconds()
        print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')
        fps = f'FPS: {1 / total:.2f}'
        cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    def create_json(self, label, conf):
        start = datetime.datetime.now()
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
        
if __name__ == "__main__":
    WEIGHT_PATH = './firesmoke2.pt'
    VEDIO_PATH = 0
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FRAME_RATE = 10
    FRAME = 10
    WAIT_TIME = 0.1
    TCP_PATH = 'tcp://192.168.1.146:8888'
    HOST = '192.168.1.146'  
    PORT = 8000  
    TCP_server = TCP_stream(tcp_path=TCP_PATH, model_path=WEIGHT_PATH, frame_width=FRAME_WIDTH, 
                            frame_height=FRAME_HEIGHT, framerate=FRAME_RATE, 
                            conf_thre=CONFIDENCE_THRESHOLD, frame = FRAME, host=HOST, port=PORT)
    
    TCP_server.stream()
