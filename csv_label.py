import json
import glob
import pandas as pd
import numpy as np
     
# 데이터 경로 설정
train_data_path = './YOLODataSet/train/images'
valid_data_path = './YOLODataSet/valid/images'
# test_data_path = './YOLODataSet/test/images'

train_label_path = './YOLODataSet/train/labels'
valid_label_path = './YOLODataSet/valid/labels'
# test_label_path = './YOLODataSet/test/labels'

# JSON 파일 경로
json_folder_path = './화재 발생 예측 영상/Validation/**'

# # json 디렉토리 파일 가져오기
json_file_path_list = glob.glob(json_folder_path,recursive=True)
json_file_path_list = [file_path for file_path in json_file_path_list if file_path.endswith('.json')]

#train,valid,test len 추출
train_len = int(0.9 * len(json_file_path_list))
valid_len = len(json_file_path_list) - train_len
# test_len = len(json_file_path_list) - train_len - valid_len
img_path_values = np.array([train_data_path] * train_len + [valid_data_path] * valid_len )
# img_path 값 섞기
np.random.shuffle(img_path_values)
# 추출된 데이터 저장할 list
data_list = []
# print(json_file_path_list)
print(len(json_file_path_list))
# json file read
for i,json_file_name in enumerate(json_file_path_list):
    with open(json_file_name, 'r', encoding='utf-8-sig') as file:
        json_data = json.load(file)
                
        #name,cls,box,resolution 추출
        filename = json_data['image']['filename']
        #.jpg 제거
        filename = filename.replace('.jpg', '')
        
        resolution_x,resolution_y = json_data['image']['resolution']
        # object가 여러개일때
        for annotations in json_data['annotations']:
            class_label = int(annotations['class']) - 1
            if class_label < 3:
                class_label = 1
            elif class_label == 3:
                class_label = 0
            elif class_label < 5:
                class_label = 2
            elif class_label < 8:
                class_label = 3
            elif class_label < 11:
                class_label = 4
            # box 좌표 추출
            if 'polygon' in annotations:
                box = []
                xpoint = [(row[0]/resolution_x) for row in annotations['polygon']] 
                ypoint = [(row[1]/resolution_y) for row in annotations['polygon']]
                for i,_ in enumerate(xpoint):
                    box.append([xpoint[i],ypoint[i]])
                box = ' '.join(map(str, [item for sublist in box for item in sublist]))
                
            if 'box' in annotations:
                lx,ly,rx,ry = annotations['box']
                #kittl 형식 box => yolo 형식 box로 변환
                x = (int(0.5 * (rx + lx)))/resolution_x
                y = (int(0.5 * (ly + ry)))/resolution_y 
                w = (rx - lx)/resolution_x
                h = (ry - ly)/resolution_y          

                box = [x,y,w,h]
                # box list [] 제거 ' ' => 공백 추출 
                box = ' '.join(map(str, box))
            data_dict = {'filename': filename, 'class': class_label, 'box': box, 'img_path' : img_path_values[i]}
            #dict 자료 추가 
            data_list.append(data_dict)
#dataframe 생성
df = pd.DataFrame(data_list)
# img_path 에서 train,valid,test value 행 추출
train_rows = df[df['img_path'] == train_data_path]
valid_rows = df[df['img_path'] == valid_data_path]
# test_rows = df[df['img_path'] == test_data_path]

#label_path 추가
if not train_rows.empty:
    df.loc[train_rows.index, 'label_path'] = train_label_path
if not valid_rows.empty:
    df.loc[valid_rows.index, 'label_path'] = valid_label_path
# if not test_rows.empty:
#     df.loc[test_rows.index, 'label_path'] = test_label_path
    
# print(df)
#dataframe save
df.to_csv('label2.csv', index=False)

# print(df.head())
           