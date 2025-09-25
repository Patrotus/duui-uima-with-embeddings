import torch
from app.embeddings.base import BaseModelEmbedder
from app.model.modality import Modality

# FIXME: DEPRECATED in favor of model specifc behaviour
class TextEmbedder(BaseModelEmbedder):
    @property
    def modality(self) -> Modality:
        return Modality.TEXT

    def __init__(self, model_name: str, model_params: dict = None):
        super().__init__(model_name, model_params)
        self._load_model()

    def preprocess(self, text: str) -> dict:
        inputs = self.processor(text, padding=True, truncation=True, return_tensors="pt").to(self.device)
        return inputs

    def generate_embedding(self, text: str) -> torch.Tensor:
        inputs = self.preprocess(text)

        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings
