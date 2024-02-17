from ultralytics import YOLO
import torch
import os
# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

resume_train = 1
# weight_path = './runs/detect/train37/weights/last.pt'
weight_path = './yolov8n.pt'
device = 0

if resume_train:
    model = YOLO(weight_path)
    # result = model.train(resume = True)
    # result = model.train(data='./YOLODataSet/data.yaml',batch = 16, epochs=100, imgsz = 640 , device = device)
    result = model.train(data='./thermography/data.yaml',batch = 16, epochs=100, imgsz = 640 , device = device)
else:    
    model = YOLO('./yolov8n.pt')
    result = model.train(data='./YOLODataSet/data.yaml',batch = 32, epochs=600, imgsz = 640)
# print(result)