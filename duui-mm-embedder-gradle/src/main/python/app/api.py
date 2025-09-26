import gc
import time

import torch
from fastapi import FastAPI, Response, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse

from .constants import STATIC_ENCODING
from .embeddings.process import process_text, process_video, process_image, process_audio
from .logger import get_logger
from .model.duui_environment import DUUIEnvironment
from .settings import Settings, DUUIMMEmbeddingsRequest, DUUIMMEmbeddingsResponse, EmbeddingResponse


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = get_logger()
        request_id = str(time.time())
        logger.info(f"Request {request_id} started: {request.method} {request.url.path}")

        if request.method == "POST":
            try:
                body_bytes = await request.body()
                max_body_log = 1000  # Max chars to log
                body_str = body_bytes.decode('utf-8')
                logger.info(f"Request {request_id} body (truncated): {body_str[:max_body_log]}{'...' if len(body_str) > max_body_log else ''}")

                request._body = body_bytes
            except Exception as e:
                logger.error(f"Error reading request body: {str(e)}")

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"Request {request_id} completed: {response.status_code} in {process_time:.3f}s")

        return response

def create_app(settings: Settings, environment: DUUIEnvironment):
    logger = get_logger()
    app = FastAPI(
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url=None,
        title=settings.annotator_name,
        description='DUUI component for Embedding generation for Multimodal modalities',
        version=settings.annotator_version,
        terms_of_service="https://www.texttechnologylab.org/legal_notice/",
        contact={
            "name": "Paul Schnürer, Thesis participant of TTLab Team",
            "url": "https://texttechnologylab.org",
            "email": "s7647597@stud.uni-frankfurt.de"
        },
        license_info={
            "name": "APGL",
            "url": "http://www.gnu.org/licenses/agpl-3.0.en.html",
        }
    )

    app.add_middleware(LoggingMiddleware)

    def tensor_to_embedding_response(tensor: torch.Tensor) -> EmbeddingResponse:
        numpy_array = tensor.cpu().numpy()
        return EmbeddingResponse(
            embedding=numpy_array.flatten().tolist(),
            shape=list(numpy_array.shape),
        )

    @app.get("/v1/typesystem")
    def get_typesystem() -> Response:
        xml = environment.type_system.to_xml()
        xml_content = xml.encode(STATIC_ENCODING)

        return Response(
            content=xml_content,
            media_type="application/xml"
        )

    @app.get("/v1/communication_layer", response_class=PlainTextResponse)
    def get_communication_layer() -> str:
        return environment.communicator

    @app.post("/v1/process")
    def post_process(request: DUUIMMEmbeddingsRequest) -> DUUIMMEmbeddingsResponse:
        errors = []
        try:
            logger.info(request)
            text_embeddings, video_embeddings, audio_embeddings, image_embeddings = [], [], [], []
            # Execute processing
            if len(request.texts.texts) > 0:
                logger.info("Processing texts")
                text_embeddings = process_text(request.texts)
            if len(request.videos.videos) > 0:
                logger.info("Processing videos")
                text_embeddings = process_video(request.videos)

            if len(request.audios.audios) > 0:
                logger.info("Processing audios")
                text_embeddings = process_audio(request.audios)

            if len(request.images.images) > 0:
                logger.info("Processing images")
                text_embeddings = process_image(request.images)

            return DUUIMMEmbeddingsResponse(
                text_embeddings=[tensor_to_embedding_response(tensor) for tensor in text_embeddings],
                video_embeddings=[tensor_to_embedding_response(tensor) for tensor in video_embeddings],
                audio_embeddings=[tensor_to_embedding_response(tensor) for tensor in audio_embeddings],
                image_embeddings=[tensor_to_embedding_response(tensor) for tensor in image_embeddings],
                # FIXME: Error handling
                errors=[],
            )

        except Exception as ex:
            logger.exception(ex)
            return DUUIMMEmbeddingsResponse(errors=[str(ex)])
        finally:
            # Taken from duui-mm
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()

    return app
