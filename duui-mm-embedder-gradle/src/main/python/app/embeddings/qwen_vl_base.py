from typing import Union

import torch
from PIL import Image
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor
import tempfile
import base64
import os

from app.embeddings import BaseModelEmbedder
from app.embeddings.base import TextEmbeddingGenerator, ImageEmbeddingGenerator, VideoEmbeddingGenerator
from app.utils.base64_utils import image_to_base64_url
from app.utils.qwen_utils import generate_message_for_type
from app.logger import get_logger

logger = get_logger()


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

    # def generate_video_embedding(self, video_base64: str) -> torch.Tensor:
    #     video_url = 'data:video/mp4;base64,' + video_base64
    #     print(video_url[:100])
    #     messages = generate_message_for_type('video', video_url)
    #     # TODO: Support video with audio aswell
    #     text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    #     image_inputs, video_inputs, video_kwargs = process_vision_info(messages, return_video_kwargs=True)
    #
    #
    #     # print(video_inputs)
    #     # print(image_inputs)
    #     # print(video_kwargs)
    #
    #     inputs = self.processor(
    #         text=[text],
    #         images=image_inputs,
    #         videos=video_inputs,
    #         padding=True,
    #         return_tensors="pt",
    #         **video_kwargs
    #     ).to(self.device)
    #
    #     with torch.no_grad():
    #         outputs = self.model(**inputs, return_dict=True, output_hidden_states=True)
    #         embeddings = outputs.last_hidden_state.mean(dim=1)
    #     return embeddings

    #####
    # Function generated: 03.11.2025 14:08 using Claude 4.5 Sonnet, based on implementation in Qwen_V2_5.py and my
    #  old implementation above.
    #####
    def generate_video_embedding(self, video_base64: str) -> torch.Tensor:
        # Save base64 video to temporary file
        video_path = None
        try:
            print("Start here")
            video_path = tempfile.mktemp(suffix=".mp4")
            with open(video_path, "wb") as f:
                f.write(base64.b64decode(video_base64))

            # Use file:// URL format for local files
            print(f"Video saved to: {video_path}")

            # Start message with video path (local file URL format for Qwen 2.5)
            content = [
                {
                    "type": "video",
                    "video": f"file://{video_path}",
                    "fps": 1.0,
                    "max_pixels": 360 * 420,
                }
            ]

            messages = [{"role": "user", "content": content}]

            # TODO: Support video with audio aswell
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            image_inputs, video_inputs, video_kwargs = process_vision_info(messages, return_video_kwargs=True)

            logger.info("Test")

            print("Test2")
            logger.info(messages)

            logger.info(image_inputs)
            logger.info(video_inputs)
            logger.info(video_kwargs)
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
                **video_kwargs,  # includes fps
            ).to(self.device)

            print(inputs)

            with torch.no_grad():
                outputs = self.model(**inputs, return_dict=True, output_hidden_states=True)
                embeddings = outputs.last_hidden_state.mean(dim=1)
                print(embeddings)

            return embeddings
        finally:
            # Cleanup: Remove temporary file
            if video_path and os.path.exists(video_path):
                try:
                    os.remove(video_path)
                    print(f"Cleaned up temporary file: {video_path}")
                except Exception as e:
                    print(f"Warning: Could not remove temporary file {video_path}: {e}")
