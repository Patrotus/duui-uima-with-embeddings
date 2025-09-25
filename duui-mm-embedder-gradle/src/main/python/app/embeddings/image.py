import torch
from PIL import Image

from app.embeddings.base import BaseModelEmbedder
from app.model.modality import Modality

# FIXME: DEPRECATED in favor of model specifc behaviour
class ImageEmbedder(BaseModelEmbedder):
    @property
    def modality(self) -> Modality:
        return Modality.IMAGE

    def __init__(self, model_name: str, model_params: dict = None, num_frames: int = 16):
        """
        Initializes an Embedder for images
        :param model_name: Name of the chosen model
        :param num_frames: Number of frames used for "video-generation"
        """
        self.num_frames = num_frames
        super().__init__(model_name, model_params)
        self._load_model()

    def _get_processor(self):
        # DEPRECATED
        pass

    # FIXME: Does not work for qwen-vl yet
    def preprocess(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocesses the image for the model.
        Extracts the pixel values from an input and generates a "video", by repeating the
        values num_frames times.
        (Taken from https://huggingface.co/facebook/vjepa2-vitl-fpc64-256)
        :param image: Image, for which embeddings should be generated
        :return: Tensor with pixel values for the image
        """
        inputs = self.processor.preprocess(images=image, return_tensors="pt").to(self.device)
        print(inputs)

        # Align pixel values to correct shape. VideoProcessor uses pixel_values_videos, ImageProcessor pixel_values
        if 'pixel_values_videos' in inputs:
            pixel_values = inputs['pixel_values_videos']
            pixel_values = pixel_values.repeat(1, self.num_frames, 1, 1, 1)
        else:
            pixel_values = inputs['pixel_values']
        return pixel_values

    def generate_embedding(self, image: Image.Image) -> torch.Tensor:
        """
        Generates embeddings for the given image.
        :param image: Image, for which embeddings should be generated
        :return: Embeddings for this image as a tensor
        """
        inputs = self.preprocess(image)

        with torch.no_grad():
            # Check for specific vison feature method, use regular model otherwise
            if hasattr(self.model, 'get_vision_features'):
                embeddings = self.model.get_vision_features(inputs)
            else:
                outputs = self.model(pixel_values=inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings
