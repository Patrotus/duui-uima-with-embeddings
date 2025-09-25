
from transformers.image_utils import load_image

from app.embeddings.qwen_vl_base import QwenVLBaseEmbedder
from app.utils.base64_utils import image_to_base64_url

hf_repo = "facebook/vjepa2-vitl-fpc64-256"
hf_repo_qwen = "Qwen/Qwen2.5-VL-3B-Instruct"
# model = AutoModel.from_pretrained(hf_repo)
# processor = AutoVideoProcessor.from_pretrained(hf_repo)
#
# #
image = load_image("https://huggingface.co/datasets/merve/coco/resolve/main/val2017/000000000285.jpg")
base64 = image_to_base64_url(image)


# generator = VJEPABaseEmbedder(hf_repo)
# embeddings = generator.generate_image_embedding(image)

qwen = QwenVLBaseEmbedder(hf_repo_qwen)
# embeddings = qwen.generate_text_embedding("Test-Text yolo uwuwuwu")
embeddings = qwen.generate_image_embedding(image)
print(embeddings.shape)
