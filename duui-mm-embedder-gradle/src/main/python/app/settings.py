from typing import Optional, List

from pydantic_settings import BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    """
    TODO
    """

    annotator_name: str
    annotator_version: str
    log_level: Optional[str]
    mm_model_cache_size: str

    class Config:
        """
        TODO
        """
        env_prefix = 'TODO'


class ImageType(BaseModel):
    """
    org.texttechnologylab.annotation.type.Image
    """
    src: str
    width: int
    height: int
    begin: int
    end: int


class VideoType(BaseModel):
    """
    org.texttechnologylab.annotation.type.Video
    """
    src: str
    length: int = -1
    fps: int = -1
    begin: int
    end: int


class AudioType(BaseModel):
    """
    org.texttechnologylab.annotation.type.Audio
    """
    src: str
    begin: int
    end: int


class TextType(BaseModel):
    """
    org.texttechnologylab.annotation.type.Text
    """
    text: str
    begin: int
    end: int


class ModelConfig(BaseModel):
    model_name: str
    model_params: dict = {}


class BaseTypeRequest(BaseModel):
    """Basis-Klasse für alle Typ-spezifischen Requests"""
    config: ModelConfig


class DUUIMMTextRequest(BaseTypeRequest):
    texts: List[TextType]


class DUUIMMAudioRequest(BaseTypeRequest):
    audios: List[AudioType]
    config: ModelConfig


class DUUIMMVideoRequest(BaseTypeRequest):
    videos: List[VideoType]


class DUUIMMImageRequest(BaseTypeRequest):
    images: List[ImageType]


class DUUIMMEmbeddingsRequest(BaseModel):
    """
    TODO: Implement docstring
    """

    images: Optional[DUUIMMImageRequest] = None

    audios: Optional[DUUIMMAudioRequest] = None

    videos: Optional[DUUIMMVideoRequest] = None

    texts: Optional[DUUIMMTextRequest] = None

    # Language of the document
    doc_lang: str

    # Length of the document
    doc_len: int


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    shape: List[int]


class DUUIMMEmbeddingsResponse(BaseModel):
    """
    TODO: Implement docstring
    """
    text_embeddings: Optional[List[EmbeddingResponse]] = None
    image_embeddings: Optional[List[EmbeddingResponse]] = None
    video_embeddings: Optional[List[EmbeddingResponse]] = None
    audio_embeddings: Optional[List[EmbeddingResponse]] = None
    errors: Optional[List[str]]
