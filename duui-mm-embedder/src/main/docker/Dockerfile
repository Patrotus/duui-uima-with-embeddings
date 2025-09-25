FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Taken from duui-mm. Carefully adapt to project specific implementation later on

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.10 python3-pip python3-setuptools python3-distutils python3-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install --upgrade pip


WORKDIR /usr/src/app

EXPOSE 9714 6659 6658


RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install ffmpeg -y


# dependencies
RUN pip install -U pip
RUN pip install setuptools wheel psutil packaging torch==2.8.0 torchvision==0.23.0  torchaudio==2.8.0
RUN pip install --upgrade setuptools
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


RUN python -c "from transformers import Qwen2_5_VLForConditionalGeneration; Qwen2_5_VLForConditionalGeneration.from_pretrained(pretrained_model_name_or_path='Qwen/Qwen2.5-VL-7B-Instruct', revision='cc594898137f460bfe9f0759e9844b3ce807cfb5')"

# copy scripts
COPY ./src/main/resources/TypeSystemMMEmbeddings.xml ./TypeSystemMMEmbeddings.xml
COPY ./src/main/python/ ./



RUN chmod +x ./start.sh


RUN echo nvidia-smi

# log level
ARG LOG_LEVEL="DEBUG"
ENV LOG_LEVEL=$LOG_LEVEL

# config
ARG MM_MODEL_CACHE_SIZE=3
ENV MM_MODEL_CACHE_SIZE=$MM_MODEL_CACHE_SIZE

# meta data
ARG ANNOTATOR_NAME="duui-mutlimodality"
ENV ANNOTATOR_NAME=$ANNOTATOR_NAME
ARG ANNOTATOR_VERSION="unset"
ENV ANNOTATOR_VERSION=$ANNOTATOR_VERSION

# Model Info
ARG MODEL_VERSION=0.1
ENV MODEL_VERSION=$MODEL_VERSION



ENTRYPOINT ["uvicorn", "duui_mm_embeddings:app", "--host", "0.0.0.0", "--port" ,"9714"]
CMD ["--workers", "1"]