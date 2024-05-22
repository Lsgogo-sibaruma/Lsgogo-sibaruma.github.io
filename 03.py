import os
import cv2
from ultralytics import YOLO

# 載入模型
model = YOLO('models/class1.pt')          #改成使用之模型

# 輸入和輸出資料夾路徑
input_folder = 'see/test'
output_folder = 'see/end'

# 確保輸出資料夾存在，如果不存在就創建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 讀取test資料夾下的所有圖片
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # 讀取圖片
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # 進行推論
        results = model(image)

        #print(results[0].boxes.cls)
        #print(results[0].boxes.xyxy)

        # 提取並印出物件的類別
        for cls in results[0].boxes.cls:  # 假設只有一個物件
            print(f"Class: {cls}")
        for box in results[0].boxes.xyxy:  # 假設只有一個物件
            x_min, y_min, x_max, y_max = box[0], box[1], box[2], box[3]
            print(f"Coordinates: ({x_min}, {y_min}, {x_max}, {y_max})")

        # 繪製檢測結果
        annotated_image = results[0].plot()

        # 將辨識結果圖片儲存到end資料夾中
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, annotated_image)

print("辨識結果已輸出到end資料夾中")
