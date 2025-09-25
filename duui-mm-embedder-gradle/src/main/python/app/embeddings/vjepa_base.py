from typing import Union, Any

import numpy as np
import torch
from PIL import Image
from transformers import AutoVideoProcessor

from app.embeddings import BaseModelEmbedder
from app.embeddings.base import ImageEmbeddingGenerator, VideoEmbeddingGenerator
from app.utils.base64_utils import base64_url_to_image


class VJEPABaseEmbedder(BaseModelEmbedder, ImageEmbeddingGenerator, VideoEmbeddingGenerator):
    def __init__(
            self,
            model_name: str,
            model_params: dict = None,
            num_image_frames: int = 16,
            num_video_sampling_frames: int = 64
    ):
        super().__init__(model_name, model_params)
        self.num_frames = num_image_frames
        self.num_video_sampling_frames = num_video_sampling_frames
        self.processor = AutoVideoProcessor.from_pretrained(model_name)

    def generate_image_embedding(self, image: Union[str, Image.Image]) -> torch.Tensor:
        if isinstance(image, str):
            image = base64_url_to_image(image)

        inputs = self.processor(image, return_tensors="pt").to(self.device)['pixel_values_videos']
        pixel_values = inputs.repeat(1, self.num_frames, 1, 1, 1)

        with torch.no_grad():
            image_embeddings = self.model.get_vision_features(pixel_values)
        return image_embeddings

    def generate_video_embedding(self, video_decoder: Any) -> torch.Tensor:
        # Current implementation from huggingface vjepa2
        # TODO: Use correct format for videos
        frame_idx = np.arange(0, self.num_video_sampling_frames)
        video = video_decoder.get_frames_at(indices=frame_idx).data
        video = self.processor(video, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            video_embeddings = self.model.get_vision_features(**video)
        return video_embeddings
