from typing import Union

import torch
from PIL import Image
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor

from app.embeddings import BaseModelEmbedder
from app.embeddings.base import TextEmbeddingGenerator, ImageEmbeddingGenerator, VideoEmbeddingGenerator
from app.utils.base64_utils import image_to_base64_url
from app.utils.qwen_utils import generate_message_for_type


class QwenVLBaseEmbedder(BaseModelEmbedder, TextEmbeddingGenerator, ImageEmbeddingGenerator, VideoEmbeddingGenerator):
    def __init__(self, model_name: str, model_params: dict = None):
        super().__init__(model_name, model_params)
        self.processor = AutoProcessor.from_pretrained(model_name)

    def generate_text_embedding(self, text: str) -> torch.Tensor:
        inputs = self.processor(text=text, padding=True, truncation=True, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

    def generate_image_embedding(self, image: Union[str, Image.Image]) -> torch.Tensor:
        if isinstance(image, str):
            messages = generate_message_for_type('image', image)
        elif isinstance(image, Image.Image):
            image_url = f'data:image/jpeg;base64,{image_to_base64_url(image)}'
            messages = generate_message_for_type('image', image_url)
        else:
            raise ValueError(f'Unsupported image type: {type(image)}. Expected str (URL/path) or PIL.Image.Image')

        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        # noinspection PyTupleAssignmentBalance
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs, return_dict=True, output_hidden_states=True)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

    def generate_video_embedding(self, video_base64: str) -> torch.Tensor:
        video_url = 'data:video/mp4;base64,' + video_base64
        messages = generate_message_for_type('video', video_url)
        # TODO: Support video with audio aswell
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        image_inputs, video_inputs, video_kwargs = process_vision_info(messages, return_video_kwargs=True)

        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
            **video_kwargs
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs, return_dict=True, output_hidden_states=True)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

