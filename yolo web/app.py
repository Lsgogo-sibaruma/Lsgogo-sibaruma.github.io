import os
from flask import Flask, request, jsonify
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# 載入模型
model = YOLO('models/class1.pt')

# 確保輸出資料夾存在，如果不存在就創建它
output_folder = 'see/end'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "沒有檔案部分"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未選擇檔案"}), 400

    if file and allowed_file(file.filename):
        # 保存上傳的圖片
        input_path = os.path.join('see/test', file.filename)
        file.save(input_path)

        # 讀取圖片
        image = cv2.imread(input_path)

        # 進行推論
        results = model(image)

        # 提取物件的類別和坐標
        classes = [int(cls) for cls in results[0].boxes.cls]
        boxes = [[float(coord) for coord in box] for box in results[0].boxes.xyxy]

        # 繪製檢測結果
        annotated_image = results[0].plot()

        # 儲存辨識結果圖片
        output_path = os.path.join(output_folder, file.filename)
        cv2.imwrite(output_path, annotated_image)

        return jsonify({
            "classes": classes,
            "boxes": boxes,
            "annotated_image_path": output_path
        })
    else:
        return jsonify({"error": "無效的檔案類型"}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='192.168.68.54', port=5000, debug=True)
