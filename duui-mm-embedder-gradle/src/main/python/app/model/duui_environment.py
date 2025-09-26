from dataclasses import dataclass

import torch
from cassis import TypeSystem


@dataclass
class DUUIEnvironment:
    """
    Data class to hold all required elements needed for the duui component. More cohesive than just passing variables.
    """
    communicator: str
    type_system: TypeSystem
    device: torch.device
