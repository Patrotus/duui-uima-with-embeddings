## TODO/WIP ##
To be able to execute the tests, executed `./gradlew build` from this directory `duui-mm-embedder-gradle` 

Afterward, tests from src/test can be executed.

To run the duui-component, navigate to the app-root folder using `cd`:
`cd src/main/python`.
In this directory run uvicorn duui_mm_embeddings:app.

Install all the requirements beforhand from the `requirements.txt`

[//]: # ([![Version]&#40;https://img.shields.io/static/v1?label=duui-multimodal\&message=0.1.0\&color=blue&#41;]&#40;https://docker.texttechnologylab.org/v2/duui-multimodal/tags/list&#41;)

[//]: # ([![Python]&#40;https://img.shields.io/static/v1?label=Python\&message=3.12\&color=green&#41;]&#40;&#41;)

[//]: # ([![Transformers]&#40;https://img.shields.io/static/v1?label=Transformers\&message=4.48.2\&color=yellow&#41;]&#40;&#41;)

[//]: # ([![Torch]&#40;https://img.shields.io/static/v1?label=Torch\&message=2.6.0\&color=red&#41;]&#40;&#41;)

[//]: # ()
[//]: # (# DUUI Multimodal Component)

[//]: # ()
[//]: # (DUUI implementation for **multimodal Hugging Face models** that support combinations of:)

[//]: # ()
[//]: # (* Text)

[//]: # (* Image)

[//]: # (* Audio)

[//]: # (* Video &#40;via uniform frame sampling and audio extraction using `ffmpeg`&#41;)

[//]: # ()
[//]: # (Supported models include variants like `microsoft/Phi-4-multimodal-instruct`.)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # ()
[//]: # (##  Supported Models)

[//]: # ()
[//]: # (| Model Name                            | Source                                                                 | Mode        | Lang  | Version      |)

[//]: # (| ------------------------------------- | ---------------------------------------------------------------------- | ----------- | ----- | ------------ |)

[//]: # (| `vllm/microsoft/Phi-4-multimodal-instruct` | 🤗 [Phi-4]&#40;https://huggingface.co/microsoft/Phi-4-multimodal-instruct&#41; | VLLM        | multi | `0af439b...` |)

[//]: # (| `microsoft/Phi-4-multimodal-instruct` | 🤗 [Phi-4]&#40;https://huggingface.co/microsoft/Phi-4-multimodal-instruct&#41; | VLLM        | multi | `0af439b...` |)

[//]: # (| `vllm/Qwen/Qwen2.5-VL-7B-Instruct`    | 🤗 [Qwen2.5-VL-7B]&#40;https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct&#41; | VLLM        | multi | `cc59489...` |)

[//]: # (| `Qwen/Qwen2.5-VL-7B-Instruct`         | 🤗                                                                     | Transformer | multi | `cc59489...` |)

[//]: # (| `Qwen/Qwen2.5-VL-7B-Instruct-AWQ`     | 🤗                                                                     | Transformer | multi | `536a357...` |)

[//]: # (| `Qwen/Qwen2.5-VL-3B-Instruct`         | 🤗                                                                     | Transformer | multi | `6628554...` |)

[//]: # (| `Qwen/Qwen2.5-VL-3B-Instruct-AWQ`     | 🤗                                                                     | Transformer | multi | `e7b6239...` |)

[//]: # (| `Qwen/Qwen2.5-VL-32B-Instruct`        | 🤗                                                                     | Transformer | multi | `7cfb30d...` |)

[//]: # (| `Qwen/Qwen2.5-VL-32B-Instruct-AWQ`    | 🤗                                                                     | Transformer | multi | `66c370b...` |)

[//]: # (| `Qwen/Qwen2.5-VL-72B-Instruct`        | 🤗                                                                     | Transformer | multi | `cd3b627...` |)

[//]: # (| `Qwen/Qwen2.5-VL-72B-Instruct-AWQ`    | 🤗                                                                     | Transformer | multi | `c8b87d4...` |)

[//]: # (| `Qwen/Qwen2.5-Omni-3B`                | 🤗                                                                     | Transformer | multi | `latest`     |)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## Supported Modes)

[//]: # ()
[//]: # (| Mode    | Description                                                         |)

[//]: # (|---------|---------------------------------------------------------------------|)

[//]: # (| `text`  | Process raw text prompts                                            |)

[//]: # (| `image` | Process images and prompt combinations                              |)

[//]: # (| `frames` | Process sequences of image frames with a shared prompt              |)

[//]: # (| `audio` | Process audio files with accompanying text prompts                  |)

[//]: # (| `video` | Process video input: extracts frames &#40;every 5th&#41;, audio, and prompt |)

[//]: # (| `frames_and_audio` | process **separate** frames and audio &#40;provide them explicitly&#41;     |)

[//]: # ()
[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## How To Use)

[//]: # ()
[//]: # (Requires the [Docker Unified UIMA Interface &#40;DUUI&#41;]&#40;https://github.com/texttechnologylab/DockerUnifiedUIMAInterface&#41;.)

[//]: # ()
[//]: # (### Start Docker Container)

[//]: # ()
[//]: # (```bash)

[//]: # (docker run -p 9714:9714 docker.texttechnologylab.org/duui-multimodal:latest)

[//]: # (```)

[//]: # ()
[//]: # (Find available image tags: [Docker Registry]&#40;https://docker.texttechnologylab.org/v2/duui-multimodal/tags/list&#41;)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## Use within DUUI)

[//]: # ()
[//]: # (### VLLM models)

[//]: # (```java)

[//]: # (composer.add&#40;)

[//]: # (    new DUUIDockerDriver.Component&#40;"docker.texttechnologylab.org/duui-mutlimodality-vllm:latest"&#41;)

[//]: # (        .withParameter&#40;"model_name", "microsoft/Phi-4-multimodal-instruct"&#41;)

[//]: # (        .withParameter&#40;"mode", "video"&#41;  // Can be: text_only, image_only, audio, frames_only, video)

[//]: # (&#41;;)

[//]: # (```)

[//]: # (### Transformer Models)

[//]: # ()
[//]: # (```java)

[//]: # (composer.add&#40;)

[//]: # (    new DUUIDockerDriver.Component&#40;"docker.texttechnologylab.org/duui-mutlimodality-transformer:latest"&#41;)

[//]: # (        .withParameter&#40;"model_name", "microsoft/Phi-4-multimodal-instruct"&#41;)

[//]: # (        .withParameter&#40;"mode", "video"&#41;  // Can be: text_only, image_only, audio, frames_only, video)

[//]: # (&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## Parameters)

[//]: # ()
[//]: # (| Name         | Description                                    |)

[//]: # (| ------------ | ---------------------------------------------- |)

[//]: # (| `model_name` | Name of the multimodal model to use            |)

[//]: # (| `mode`       | Processing mode: text\_only, image\_only, etc. |)

[//]: # (| `prompt`     | Prompt passed alongside media inputs           |)

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## Cite)

[//]: # ()
[//]: # (If you want to use the DUUI image, please cite the following:)

[//]: # ()
[//]: # (**Leonhardt et al. &#40;2023&#41;**)

[//]: # (*"Unlocking the Heterogeneous Landscape of Big Data NLP with DUUI."*)

[//]: # (Findings of the Association for Computational Linguistics: EMNLP 2023, 385–399.)

[//]: # (\[[LINK]&#40;https://aclanthology.org/2023.findings-emnlp.29&#41;] \[[PDF]&#40;https://aclanthology.org/2023.findings-emnlp.29.pdf&#41;])

[//]: # ()
[//]: # (---)

[//]: # ()
[//]: # (## BibTeX)

[//]: # ()
[//]: # (```bibtex)

[//]: # (@inproceedings{Leonhardt:et:al:2023,)

[//]: # (  title     = {Unlocking the Heterogeneous Landscape of Big Data {NLP} with {DUUI}},)

[//]: # (  author    = {Leonhardt, Alexander and Abrami, Giuseppe and Baumartz, Daniel and Mehler, Alexander},)

[//]: # (  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2023},)

[//]: # (  year      = {2023},)

[//]: # (  address   = {Singapore},)

[//]: # (  publisher = {Association for Computational Linguistics},)

[//]: # (  url       = {https://aclanthology.org/2023.findings-emnlp.29},)

[//]: # (  pages     = {385--399},)

[//]: # (  pdf       = {https://aclanthology.org/2023.findings-emnlp.29.pdf})

[//]: # (})

[//]: # ()
[//]: # (@misc{abusaleh:2025,)

[//]: # (  author         = {Abusaleh, Ali},)

[//]: # (  title          = {Multimodal Inference as {DUUI} Component},)

[//]: # (  year           = {2025},)

[//]: # (  howpublished   = {https://github.com/texttechnologylab/duui-uima/tree/main/duui-multimodal})

[//]: # (})


