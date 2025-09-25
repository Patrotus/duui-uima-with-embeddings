from typing import List, Optional, Any, Type, Callable

import torch
from transformers.image_utils import load_image

from app.embeddings.base import TextEmbeddingGenerator, ImageEmbeddingGenerator, VideoEmbeddingGenerator, \
    AudioEmbeddingGenerator
from app.embeddings.model_factory import ModelFactory
from app.settings import DUUIMMTextRequest, DUUIMMImageRequest, DUUIMMVideoRequest, DUUIMMAudioRequest, BaseTypeRequest


def process_request(
        request: Optional[BaseTypeRequest],
        generator: Type,
        generator_method: str,
        data_attribute: str,
        processor: Callable[[Any], Any]
) -> List[torch.Tensor]:
    # Check whether the request even contains any data
    if not request or not getattr(request, data_attribute):
        return []

    # Try to get embedder class from the factory
    embedder_class = ModelFactory.get_embedder_class(request.config.model_name)

    # Check whether the embedder foumd even support processing of the given data type
    if not issubclass(embedder_class, generator):
        raise ValueError(f"Model {request.config.model_name} does not support processing of {data_attribute}")

    embedder = embedder_class(
        model_name=request.config.model_name,
        model_params=request.config.model_params
    )

    # Gets a reference to the data and the generator
    generator = getattr(embedder, generator_method)
    data = getattr(request, data_attribute)

    # Extracts data and generates embedding for each item
    return [
        generator(processor(item))
        for item in data
    ]


# FIXME: Error handling, when an exception is thrown in processing
# FIXME: Assign one embedding result to corresponding request

def process_text(request: Optional[DUUIMMTextRequest]) -> List[torch.Tensor]:
    return process_request(
        request,
        TextEmbeddingGenerator,
        'generate_text_embedding',
        'texts',
        lambda x: x.text
    )


# FIXME: Allow handling of image type and image by src
def process_image(request: Optional[DUUIMMImageRequest]) -> List[torch.Tensor]:
    return process_request(
        request,
        ImageEmbeddingGenerator,
        'generate_image_embedding',
        'images',
        lambda x: load_image(x.src)
    )


def process_video(request: Optional[DUUIMMVideoRequest]) -> List[torch.Tensor]:
    return process_request(
        request,
        VideoEmbeddingGenerator,
        'generate_video_embedding',
        'videos',
        lambda x: x.src
    )


def process_audio(request: Optional[DUUIMMAudioRequest]) -> List[torch.Tensor]:
    return process_request(
        request,
        AudioEmbeddingGenerator,
        'generate_audio_embedding',
        'audios',
        lambda x: x.src
    )
