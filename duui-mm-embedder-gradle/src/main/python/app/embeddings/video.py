from torch import Tensor

from app.embeddings.base import BaseModelEmbedder


# FIXME: DEPRECATED in favor of model specifc behaviour
class VideoEmbedder(BaseModelEmbedder):
    def __init__(self, model_name: str, model_params: dict = None):
        super().__init__(model_name, model_params)
        self._load_model()

    def preprocess(self, video_url: str) -> Tensor:
        pass
        # FIXME: Taken form facebookvjepa. Not generic enough
        # vr = VideoDecoder(video_url)
        # # TODO: Implement better methods for choosing frames
        # frame_idx = np.arange(0, 64) # choosing some frames. here, you can define more complex sampling strategy
        # video = vr.get_frames_at(indices=frame_idx).data  # T x C x H x W
        # video = self.processor(video, return_tensors="pt").to(self.model.device)
        # return video

    def generate_embedding(self, video_url: str) -> Tensor:
        pass
        # inputs = self.preprocess(video_url)
        #
        # with torch.no_grad():
        #     video_embeddings = self.model.get_vision_features(inputs)
        # return video_embeddings
