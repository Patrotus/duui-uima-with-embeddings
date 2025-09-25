import librosa
import torch

from app.embeddings.base import BaseModelEmbedder
from app.model.modality import Modality

# FIXME: DEPRECATED in favor of model specifc behaviour
class AudioEmbedder(BaseModelEmbedder):
    @property
    def modality(self) -> Modality:
        return Modality.AUDIO

    def __init__(self, model_name: str, model_params: dict = None, sample_rate: int = 16_000):
        """
        Initializes an Embedder for images
        :param model_name: Name of the chosen model
        """
        self.sample_rate = sample_rate
        super().__init__(model_name, model_params)
        self._load_model()

    def preprocess(self, audio_path: str) -> torch.Tensor:
        waveform, _ = librosa.load(audio_path, sr=self.sample_rate)

        inputs = (
            self.processor(
                waveform,
                sampling_rate=self.sample_rate,
                return_tensors="pt",
                padding=True)
            .to(self.device)
        )

        return inputs.input_values

    def generate_embedding(self, audio_path: str) -> torch.Tensor:
        inputs = self.preprocess(audio_path)

        with torch.no_grad():
            outputs = self.model(inputs)
            embeddings = torch.mean(outputs.last_hidden_state, dim=1)

        return embeddings
