from ultralytics import YOLO

# Load a pretrained YOLOv8n model with CUDA
model = YOLO('Thermal.pt')

# Define path to video file
source = './firevedio12.mp4'

# Run inference on the source
model.predict(source, save=True, imgsz=(640,480), conf=0.6)
