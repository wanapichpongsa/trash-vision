from ultralytics import YOLO

model = YOLO("yolo11n.pt")

# YOLO Dataset Guide: https://docs.ultralytics.com/datasets/detect/
results = model.train(data="../data/dataset.yaml", epochs=100, imgsz=640)
print(results)