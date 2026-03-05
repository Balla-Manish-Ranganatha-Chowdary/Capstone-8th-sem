import torch
import torch.nn as nn
from torchvision.models.segmentation import deeplabv3_resnet50

def get_deeplabv3_4channel(num_classes=4):
    """
    Returns a DeepLabV3+ ResNet50 model modified to accept 4 input channels (R, G, B, SWIR)
    and output `num_classes` masks.
    """
    # Load a pretrained DeepLabV3+ model
    model = deeplabv3_resnet50(weights='DEFAULT')
    
    # Modify the first convolutional layer of the ResNet backbone to take 4 channels
    # The original first conv layer is: Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    old_conv = model.backbone.conv1
    new_conv = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
    
    with torch.no_grad():
        # Copy the weights for the first 3 channels (RGB)
        new_conv.weight[:, :3, :, :] = old_conv.weight
        # Initialize the 4th channel (SWIR) weights as the mean of the RGB channels
        new_conv.weight[:, 3:4, :, :] = old_conv.weight.mean(dim=1, keepdim=True)
        
    model.backbone.conv1 = new_conv
    
    # Modify the classifier to output `num_classes` (Barren, Buildings, Water, Vegetation)
    # The classifier is an ASPP module followed by convolutions. We change the last conv layer.
    model.classifier[4] = nn.Conv2d(256, num_classes, kernel_size=(1, 1), stride=(1, 1))
    
    # Also modify the aux classifier if present
    if model.aux_classifier is not None:
        model.aux_classifier[4] = nn.Conv2d(256, num_classes, kernel_size=(1, 1), stride=(1, 1))
        
    return model

if __name__ == "__main__":
    # Test the model creation
    model = get_deeplabv3_4channel(num_classes=4)
    # Batch size 2, 4 channels (R,G,B,SWIR), 256x256 image
    dummy_input = torch.randn(2, 4, 256, 256) 
    output = model(dummy_input)
    print("Output shape:", output['out'].shape) # Expected: (2, 4, 256, 256)
