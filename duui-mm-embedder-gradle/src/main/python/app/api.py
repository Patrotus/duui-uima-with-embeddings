import gc
import time
import json

import torch
from fastapi import FastAPI, Response, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse

from .constants import STATIC_ENCODING
from .embeddings.process import process_text, process_video, process_image, process_audio
from .logger import get_logger
from .model.duui_environment import DUUIEnvironment
from .settings import Settings, DUUIMMEmbeddingsRequest, DUUIMMEmbeddingsResponse, EmbeddingResponse, LLMResult


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

    def _generate_dummy_ref() -> str:
        return str(time.time())

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
        logger.info("Started request")
        try:
            logger.info(request)
            text_embeddings, video_embeddings, audio_embeddings, image_embeddings = [], [], [], []
            # Execute processing
            if request.texts is not None and len(request.texts.texts) > 0:
                logger.info("Processing texts")
                try:
                    text_embeddings = process_text(request.texts)
                except Exception as text_ex:
                    logger.error(f"Error processing texts: {text_ex}", exc_info=True)
                    dummy_ref = _generate_dummy_ref()
                    error_result = LLMResult(
                        meta=json.dumps({"error": "Text processing failed", "detail": str(text_ex)}),
                        prompt_ref=dummy_ref,
                        message_ref=dummy_ref
                    )
                    errors.append(error_result)

            if request.videos is not None and len(request.videos.videos) > 0:
                logger.info("Processing videos")
                try:
                    video_embeddings = process_video(request.videos)
                except Exception as video_ex:
                    logger.error(f"Error processing videos: {video_ex}", exc_info=True)
                    dummy_ref = _generate_dummy_ref()
                    error_result = LLMResult(
                        meta=json.dumps({"error": "Video processing failed", "detail": str(video_ex)}),
                        prompt_ref=dummy_ref,
                        message_ref=dummy_ref
                    )
                    errors.append(error_result)

            if request.audios is not None and len(request.audios.audios) > 0:
                logger.info("Processing audios")
                try:
                    audio_embeddings = process_audio(request.audios)
                except Exception as audio_ex:
                    logger.error(f"Error processing audios: {audio_ex}", exc_info=True)
                    dummy_ref = _generate_dummy_ref()
                    error_result = LLMResult(
                        meta=json.dumps({"error": "Audio processing failed", "detail": str(audio_ex)}),
                        prompt_ref=dummy_ref,
                        message_ref=dummy_ref
                    )
                    errors.append(error_result)

            if request.images is not None and len(request.images.images) > 0:
                logger.info("Processing images")
                try:
                    image_embeddings = process_image(request.images)
                except Exception as image_ex:
                    logger.error(f"Error processing images: {image_ex}", exc_info=True)
                    dummy_ref = _generate_dummy_ref()
                    error_result = LLMResult(
                        meta=json.dumps({"error": "Image processing failed", "detail": str(image_ex)}),
                        prompt_ref=dummy_ref,
                        message_ref=dummy_ref
                    )
                    errors.append(error_result)

            logger.info("Reached response")

            response =  DUUIMMEmbeddingsResponse(
                text_embeddings=[tensor_to_embedding_response(tensor) for tensor in text_embeddings],
                video_embeddings=[tensor_to_embedding_response(tensor) for tensor in video_embeddings],
                audio_embeddings=[tensor_to_embedding_response(tensor) for tensor in audio_embeddings],
                image_embeddings=[tensor_to_embedding_response(tensor) for tensor in image_embeddings],
                errors=errors if errors else None,
            )
            # print(response)
            return response

        except Exception as ex:
            logger.exception(ex)
            # print(ex)
            print(ex)
            return DUUIMMEmbeddingsResponse(errors=[{}])
            return DUUIMMEmbeddingsResponse(errors=[str(ex)])
        finally:
            # Taken from duui-mm
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()

    return app
