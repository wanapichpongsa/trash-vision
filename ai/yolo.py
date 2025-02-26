from ultralytics import YOLO

model = YOLO("yolo11n.pt")

# https://github.com/ultralytics/JSON2YOLO protocol to make custom .yaml dataset.
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
print(results)