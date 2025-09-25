import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Set, Union
import torch
from PIL import Image
from transformers import AutoModel

from app.logger import get_logger
from app.model.modality import Modality
from app.utils.torch_utils import get_torch_device


class BaseModelEmbedder(ABC):
    # Class cache for loaded models. Caches all models of deviated classes in this base cache
    _model_cache = {}

    def __init__(self, model_name: str, model_params: Dict = None, device: str = None):
        self.model_name = model_name
        self.model_params = model_params or {}
        self.device = device or get_torch_device()
        self.model = None
        self.processor = None
        self.logger = get_logger()
        self._load_model()

    @property
    def supported_modalities(self) -> Set[Modality]:
        modalities = set()

        interface_to_modality = {
            ImageEmbeddingGenerator: Modality.IMAGE,
            TextEmbeddingGenerator: Modality.TEXT,
            VideoEmbeddingGenerator: Modality.VIDEO,
            AudioEmbeddingGenerator: Modality.AUDIO
        }

        for interface in interface_to_modality:
            if isinstance(self, interface):
                modalities.add(interface_to_modality[interface])

        return modalities

    def _generate_cache_key(self) -> str:
        params = json.dumps(self.model_params, sort_keys=True)
        return f'{self.model_name}_{params}'

    def _load_model(self):
        """
        Loads the model specified in the constructor. Uses a simple caching mechanism
        """
        cache_key = self._generate_cache_key()

        if cache_key not in self._model_cache:
            self.logger.debug(f'Cache miss for model "{self.model_name}"')
            self._load_model_into_cache()
        else:
            self.logger.debug(f'Cache hit for model "{self.model_name}"')
            self._retrieve_model_from_cache()

    def _load_model_into_cache(self):
        model = AutoModel.from_pretrained(self.model_name)
        self._use_model_and_add_to_cache(model)

    def _use_model_and_add_to_cache(self, model: Any):
        """
        Adds a specified model and processor to the cache and sets them as class model and processor.
        """
        cache_key = self._generate_cache_key()
        BaseModelEmbedder._model_cache[cache_key] = model
        self.model = model

    def _retrieve_model_from_cache(self):
        """
        Retrieves model/processor from the cache and sets them as class model and processor.
        """
        cache_key = self._generate_cache_key()
        self.model = BaseModelEmbedder._model_cache[cache_key]


class ImageEmbeddingGenerator(ABC):
    @abstractmethod
    def generate_image_embedding(self, image: Union[str, Image.Image]) -> torch.Tensor:
        pass


class TextEmbeddingGenerator(ABC):
    @abstractmethod
    def generate_text_embedding(self, text: str) -> torch.Tensor:
        pass


class VideoEmbeddingGenerator(ABC):
    @abstractmethod
    def generate_video_embedding(self, video_base64: str) -> torch.Tensor:
        pass


class AudioEmbeddingGenerator(ABC):
    @abstractmethod
    def generate_audio_embedding(self, audio_base64: str) -> torch.Tensor:
        pass
