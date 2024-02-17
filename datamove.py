import pandas as pd
import glob
import os
import shutil

csv_file_path = './label2.csv'
df = pd.read_csv(csv_file_path)

img_data_folder_path = './화재 발생 예측 영상/Validation/**'
img_data_list = glob.glob(img_data_folder_path,recursive=True)
img_data_list = [file_path for file_path in img_data_list if file_path.endswith('.jpg')]

print(len(img_data_list))
# 이미 이동한 파일을 추적하기 위한 집합 생성
moved_files = set()

for img_path in img_data_list:
    # 파일 이름과 확장자 분리
    img_name, img_ext = os.path.splitext(os.path.basename(img_path))
    # 데이터 프레임에서 파일 이름 가져오기
    df_file_names = df['filename']
    
     # 파일 이름이 데이터 프레임에 있는지 확인하고 이동하지 않은 파일인지 확인
    if img_name in df_file_names.values and img_name not in moved_files:
        # 데이터 프레임에서 해당 파일의 img_path 가져오기
        img_path_value = df[df_file_names == img_name]['img_path'].values[0]
        
        # 파일을 이동할 폴더 경로 설정
        destination_folder = img_path_value
        
        # 파일을 이동할 경로 설정
        destination_path = os.path.join(destination_folder, os.path.basename(img_path))

        # 파일 이동
        shutil.move(img_path, destination_path)
        
        # 이동한 파일을 추적하기 위해 집합에 추가
        moved_files.add(img_name)
        
# 각 행마다 파일 생성
for _, row in df.iterrows():
    # 파일 경로 가져오기
    filename = f'{row['label_path']}/{row['filename']}.txt'
    # 클래스 상자 값 가져오기 
    box_values = row['box']
    cls_values = row['class'] 
    # 파일 열기 및 쓰기 모드로 설정
    with open(filename, 'a') as f:
        # 클래스 상자 값을 파일에 작성
        f.write(f"{cls_values} {box_values}\n")