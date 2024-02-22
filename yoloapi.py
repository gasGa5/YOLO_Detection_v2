from ultralytics import YOLO
import yaml
import glob
import random
import pandas as pd
import json

# source = 'https://www.youtube.com/watch?v=1o6i3tPEcLM&t=13s'
# yaml_file_path = './thermography/data.yaml'
# folder_path = './Fire_Smoke_Detection.v1i.yolov8/train/images'
# Input_type_URL(source)
    
# def yaml_data_extract(yaml_data_path, sample_num):
#     with open(yaml_data_path, 'r') as yaml_file:
#         data = yaml.safe_load(yaml_file)
#     test_img_path = glob.glob(f'{data['test']}/*.jpg')
#     selected_img = random.sample(test_img_path, sample_num)

#     return selected_img

# def Input_type_yaml(input, model, sample_num, show = True, save = True):
#     source = yaml_data_extract(input,sample_num)
#     results = model.predict(source, show = show, save = save)
#     return results

def Input_type_URL(input, model, show = True, save = True):
    results = model.predict(input, model, show = show, save = save)
    return results

def Input_type_img(input, model, show = True, save = True):
    results = model.predict(input, save = save)
    return results

def Output_extract(results):
    df_list = []  # 데이터 프레임을 저장할 리스트 생성
    for result in results:
        shape = result.boxes.cls.shape
        if shape[0] != 0:
            jsons = result.tojson()
            df = pd.read_json(jsons)
            df_list.append(df)  # 생성된 데이터 프레임을 리스트에 추가
    # 모든 데이터 프레임을 하나로 합치기
    object = pd.concat(df_list)  
    return object
    # return object['name'], object['class'], object['confidence'], object['box']

def fire_dection(name,  conf, threshold):
    if conf > threshold:    
        if name == 'fire':
            return True
    else:
        return False

def dection_loop(results):
    objects = Output_extract(results)
    print(objects)
    for name,confidence,box in zip(objects['name'], objects['confidence'], objects['box']):
        if  fire_dection(name, confidence, 0.7):
            json_data  = create_json(name, confidence, box)
            print(json_data)
            # print(f'cls:{name}, conf:{confidence}, box:{box}')
        # print('fire')

def create_json(name,conf,box):
    data = {
        'name': name,
        'conf': conf,
        'box': box
    }
    json_data = json.dumps(data)
    
    return json_data
         
# if __name__ == "main":
model = YOLO('./firesmoke3.pt')
# img = './fire.v2i.yolov8/train/images'
img = './firevedio5.mp4'
# test_img_path = glob.glob(f'{img}/*.jpg')
results = Input_type_URL(img, model)
# print(results)