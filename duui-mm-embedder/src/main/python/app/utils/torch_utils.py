import torch
from torch import device


def get_torch_device() -> device:
    """
    Uses a cuda device, should it be available. Defaults to cpu
    """
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
