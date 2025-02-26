import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class SelfAttention(nn.Module):
  def __init__(self, in_dim):
    super(SelfAttention, self).__init__() # Call the parent class constructor

    # in_dim // 8 dimension reduction for efficiency; "Attention Is All You Need" method of Multi-Head Attention
    # kernel_size=1 for 1x1 convolutions aka "pointwise convolutions"
    # pointwise convolutions learnable linearly transformations for each position Q, K and V
    self.query = nn.Conv2d(in_dim, in_dim // 8, kernel_size=1)
    self.key = nn.Conv2d(in_dim, in_dim // 8, kernel_size=1)
    self.value = nn.Conv2d(in_dim, in_dim, kernel_size=1) # V contains actual features hence no dimension reduction
    self.gamma = nn.Parameter(torch.zeros(1)) # > 0 uses attention

  def forward(self, x):
    batch_size, C, H, W = x.size() # Get 

    # Calculate Q, K, V
    Q = self.query(x).view(batch_size, -1, H * W).permute(0, 2, 1)  # (B, N, C)
    K = self.key(x).view(batch_size, -1, H * W)                     # (B, C, N)
    V = self.value(x).view(batch_size, -1, H * W)                   # (B, C, N)

    # Attention Weights
    attention = torch.bmm(Q, K) # biased matrix multiplication -> (B, N, N)
    attention = F.softmax(attention, dim=-1)

    # Apply attention to V
    out = torch.bmm(V, attention.permute(0, 2, 1))
    out = out.view(batch_size, C, H, W)

    # Weighted sum of original input and attention output
    out = self.gamma * out + x
    return out

class AttentionResNet(nn.Module):
  def __init__(self, num_classes):
    """
    During transfer learning, we need pre-trained feature extractors,
    But remove task-specific classifiers.
    """
    super(AttentionResNet, self).__init__()
    
    # Load Pretrained ResNet (ResNet or MobileNet better?) or YOLO: https://github.com/ultralytics
    """
    YOLO: Divides image into grids, predicts bounding boxes and classes for each grid
    Faster Region-CNN
    Masked Region-CNN
    EfficientNet
    RetinaNet
    """
    self.resnet = models.resnet18(pretrained=True) # 1,000 classes from ImageNet
    self.resnet = nn.Sequential(*list(self.resnet.children())[:-2])  # Remove classifiers
    
    # Add Self-Attention after feature extraction
    self.attention = SelfAttention(in_dim=512)  # ResNet18 last layer output channels = 512
    
    # Global Average Pooling and Classifier to reduce spatial dimensions and output class probabilities
    self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(512, num_classes)

  # has to be called forward for nn.Module
  def forward(self, x):
    x = self.resnet(x)        # Extract features using ResNet
    x = self.attention(x)     # Apply self-attention
    x = self.global_pool(x)   # Global average pooling
    x = torch.flatten(x, 1)   # Flatten for fully connected layer
    x = self.fc(x)            # Classifier
    
    return x
  
from ultralytics import YOLO
class AttentionYOLO(nn.Module):
  def __init__(self, num_classes):
    super(AttentionYOLO, self).__init__()

    self.yolo = YOLO("yolo11n.pt")

    # Freeze YOLO parameters to prevent them from being updated during training
    for param in self.yolo.parameters():
      param.requires_grad = False

    self.attention = SelfAttention(in_dim=512)

    self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(512, num_classes)

  def forward(self, x):
    features = self.yolo.model.backbone(x) # backbone does not exist.

    # Apply attention to last feature map
    x = self.attention(features[-1])
    x = self.global_pool(x)
    x = torch.flatten(x, 1)
    x = self.fc(x)

    return x