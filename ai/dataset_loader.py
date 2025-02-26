import os
from PIL import Image
from torch.utils.data import Dataset

# Custom Dataset class using standards for DataLoader from torch.utils.data
class WasteDataset(Dataset):
    def __init__(self, root_dir, transform=None):
      self.root_dir = root_dir
      self.transform = transform
      self.image_paths = []
      self.labels = []

      # Assign numeric labels to each category
      self.class_to_idx = {category: idx for idx, category in enumerate(os.listdir(root_dir))}
      
      # Flatten images and labels into lists
      for category, label in self.class_to_idx.items():
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
          for image_file in os.listdir(category_path):
            self.image_paths.append(os.path.join(category_path, image_file))
            self.labels.append(label)

    def __len__(self):
      return len(self.image_paths)

    def __getitem__(self, idx):
      image_path = self.image_paths[idx]
      image = Image.open(image_path).convert("RGB")
      label = self.labels[idx]

      if self.transform:
          image = self.transform(image)
      
      return image, label

"""
Example Output:
Batch Image Shape: torch.Size([32, 3, 224, 224])
Batch Labels: tensor([0, 1, 0, 2, ...])  # Corresponding class labels for each image
^ Is it better to have a tensor of categories as indexes?
"""