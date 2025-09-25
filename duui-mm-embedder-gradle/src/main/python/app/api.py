import gc
import torch
from fastapi import FastAPI, Response
from starlette.responses import PlainTextResponse

from constants import STATIC_ENCODING
from embeddings.process import process_text, process_video, process_image, process_audio
from logger import get_logger
from model.DUUIEnvironment import DUUIEnvironment
from settings import Settings, DUUIMMEmbeddingsRequest, DUUIMMEmbeddingsResponse, EmbeddingResponse


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
            # Execute processing
            text_embeddings = process_text(request.texts)
            video_embeddings = process_video(request.videos)
            audio_embeddings = process_audio(request.audios)
            image_embeddings = process_image(request.images)

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
