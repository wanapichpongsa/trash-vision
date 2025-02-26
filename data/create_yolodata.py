import os
import shutil

# TODO: .txt labels with class id: x_center, y_center, width, height except image no objects (from 0-1, divide by image width and height if pixels, jpg probably)

def create_dirs() -> None:
  if not os.path.isdir("dataset-YOLO"):
    os.makedirs("dataset-YOLO")

  if not os.path.isdir("dataset-YOLO/images"):
    os.makedirs("dataset-YOLO/images")
    os.makedirs("dataset-YOLO/images/train")
    os.makedirs("dataset-YOLO/images/val")

  if not os.path.isdir("dataset-YOLO/labels"):
    os.makedirs("dataset-YOLO/labels")
    os.makedirs("dataset-YOLO/labels/train")
    os.makedirs("dataset-YOLO/labels/val")

def migrate_data(dataset_path) -> list:
  classes = []
  for item in os.listdir(dataset_path):
    if os.path.isdir(os.path.join(dataset_path, item)):
      sub_classes = migrate_data(os.path.join(dataset_path, item))
      classes.extend(sub_classes) # Adds all classes found in subdirectories
      classes.append(item)        # Adds current directory name
    elif item.endswith(".jpg"):
      shutil.move(os.path.join(dataset_path, item), os.path.join("dataset-YOLO/images/train", item))
    elif item.endswith(".txt"):
      shutil.move(os.path.join(dataset_path, item), os.path.join("dataset-YOLO/labels/train", item))
  return classes

if __name__ == "__main__":
  create_dirs()
  all_classes = migrate_data("dataset-resized")
  all_classes = sorted(list(set(all_classes)))
  print(f"Found classes: {all_classes}")

  if not os.path.isfile("dataset.yaml"):
    classes_str = ""
    for i, item in enumerate(all_classes):
      classes_str += f"  {i}: {item}\n"

    with open("dataset.yaml", "w") as f:
      f.write('path: ./dataset-YOLO\n'
              'train: images/train\n'
              'val: images/val\n'
              'names:\n'
              f'{classes_str}')