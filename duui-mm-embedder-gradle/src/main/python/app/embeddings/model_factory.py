from typing import Type

from app.embeddings import BaseModelEmbedder
from app.embeddings.qwen_vl_base import QwenVLBaseEmbedder
from app.embeddings.vjepa_base import VJEPABaseEmbedder


class ModelFactory:
    MAPPINGS = {
        'qwen': QwenVLBaseEmbedder,
        'facebook/vjepa': VJEPABaseEmbedder
        # TODO: Implement basic implementations for other models
    }

    @classmethod
    def get_embedder_class(cls, model_name: str) -> Type[BaseModelEmbedder]:
        for prefix, embedder_clazz in cls.MAPPINGS.items():
            if model_name.lower().startswith(prefix.lower()):
                return embedder_clazz

        # FIXME: Implement missing implementations for default model (should work)?

        raise ValueError(f"No implementation found for {model_name}")