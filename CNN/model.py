import torch
import torch.nn as nn
import torch.nn.functional as F
import segmentation_models_pytorch as smp
import logging

class CombinedLoss(nn.Module):
    """Combined loss: 0.5 * CrossEntropyLoss + 0.5 * DiceLoss"""
    def __init__(self, class_weights=None, use_focal=False, focal_gamma=2.0):
        super().__init__()
        self.use_focal = use_focal
        
        if use_focal:
            self.ce_focal_loss = smp.losses.FocalLoss(
                mode=smp.losses.MULTICLASS_MODE, 
                gamma=focal_gamma
            )
        else:
            self.ce_loss = nn.CrossEntropyLoss(weight=class_weights)
            
        self.dice_loss = smp.losses.DiceLoss(mode=smp.losses.MULTICLASS_MODE)

    def forward(self, logits, targets):
        if self.use_focal:
            ce_loss_val = self.ce_focal_loss(logits, targets)
        else:
            ce_loss_val = self.ce_loss(logits, targets)
            
        dice_loss_val = self.dice_loss(logits, targets)
        return 0.5 * ce_loss_val + 0.5 * dice_loss_val

class ISROSegmentationModel(nn.Module):
    """
    DeepLabV3+ model adapted for 5-channel satellite imagery.
    Channels: Red, Green, Blue, SWIR1, SWIR2
    """
    def __init__(self, backbone='resnet50', num_classes=8, pretrained=True):
        super().__init__()
        self.num_classes = num_classes
        self.backbone_name = backbone
        
        self.model = smp.DeepLabV3Plus(
            encoder_name=backbone,
            encoder_weights='imagenet' if pretrained else None,
            in_channels=5,
            classes=num_classes,
        )
        
        if pretrained:
            self.channel_weights_init()

    def channel_weights_init(self):
        """
        Copies pretrained RGB weights into the SWIR channels by averaging
        existing 3-channel conv1 weights and assigning to channels 4 and 5.
        """
        # Find the first convolution layer
        first_conv = None
        for module in self.model.encoder.modules():
            if isinstance(module, nn.Conv2d):
                first_conv = module
                break
                
        if first_conv is not None and first_conv.in_channels == 5:
            with torch.no_grad():
                weights = first_conv.weight.data
                # SMP usually copies the weights for extra channels when in_channels > 3 and pre-trained, 
                # but we'll fulfill the requirement of averaging RGB explicitly
                rgb_weights = weights[:, :3, :, :]
                avg_rgb = torch.mean(rgb_weights, dim=1, keepdim=True)
                # Assign to SWIR1 (idx 3) and SWIR2 (idx 4)
                first_conv.weight.data[:, 3:4, :, :] = avg_rgb
                first_conv.weight.data[:, 4:5, :, :] = avg_rgb
                logging.info(f"Initialized SWIR channels by averaging RGB weights in {self.backbone_name}")
        else:
            logging.warning("Could not find suitable first 5-channel Conv2d layer for SWIR initialization.")

    def forward(self, x):
        """
        Args:
            x: Tensor of shape (B, 5, H, W)
        Returns:
            logits tensor of shape (B, num_classes, H, W)
        """
        return self.model(x)

    def predict_mask(self, x):
        """
        Args:
            x: Tensor of shape (B, 5, H, W)
        Returns:
            argmax class map (B, H, W)
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            return torch.argmax(logits, dim=1)

    def predict_proba(self, x):
        """
        Args:
            x: Tensor of shape (B, 5, H, W)
        Returns:
            softmax probability map (B, num_classes, H, W)
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            return F.softmax(logits, dim=1)

def compute_metrics(pred_mask: torch.Tensor, true_mask: torch.Tensor, num_classes: int) -> dict:
    """
    Computes semantic segmentation metrics.
    
    Args:
        pred_mask: Tensor of shape (B, H, W) or (H, W)
        true_mask: Tensor of shape (B, H, W) or (H, W)
        num_classes: int
        
    Returns:
        dict: Configuration of metrics.
    """
    pred_mask = pred_mask.flatten()
    true_mask = true_mask.flatten()
    
    # Ignore background class if needed, but per requirements we compute for all
    hist = torch.bincount(
        num_classes * true_mask + pred_mask, 
        minlength=num_classes ** 2
    ).view(num_classes, num_classes).float()
    
    # Per-class evaluation
    intersection = torch.diag(hist)
    target_sum = hist.sum(dim=1)
    pred_sum = hist.sum(dim=0)
    union = target_sum + pred_sum - intersection
    
    # Per-class IoU
    per_class_iou = intersection / (union + 1e-6)
    
    # Per-class F1 (Dice)
    per_class_f1 = 2 * intersection / (target_sum + pred_sum + 1e-6)
    
    # Overall metrics
    pixel_accuracy = intersection.sum() / (hist.sum() + 1e-6)
    mean_iou = torch.nanmean(per_class_iou)
    mean_f1 = torch.nanmean(per_class_f1)
    
    return {
        'mean_iou': mean_iou.item(),
        'per_class_iou': per_class_iou.tolist(),
        'pixel_accuracy': pixel_accuracy.item(),
        'mean_f1': mean_f1.item(),
        'per_class_f1': per_class_f1.tolist()
    }

def build_model(config: dict) -> ISROSegmentationModel:
    """
    Builds the model from a configuration dictionary.
    """
    backbone = config.get('backbone', 'resnet50')
    num_classes = config.get('num_classes', 8)
    pretrained = config.get('pretrained', True)
    
    model = ISROSegmentationModel(
        backbone=backbone, 
        num_classes=num_classes, 
        pretrained=pretrained
    )
    return model

def load_pretrained(model: ISROSegmentationModel, checkpoint_path: str) -> ISROSegmentationModel:
    """
    Loads pretrained weights from a checkpoint path.
    """
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    logging.info(f"Loaded model checkpoint from {checkpoint_path}")
    return model
