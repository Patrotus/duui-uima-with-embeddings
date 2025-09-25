from functools import lru_cache

import torch

from app.settings import Settings
from app.logger import get_logger, initialize_logger
from app.utils.lua_communication import load_lua_communicator
from app.utils.typessystem_loader import load_typesystem_from_file
from app.api import create_app
from app.model import DUUIEnvironment

# TODO: Use settings from start.sh or Dockerfile, instead of hardcoding
settings = Settings(
    annotator_name='DUUI Multi Modal Embeddings',
    annotator_version='0.0.1',
    # TODO: Could be int? Taken from duui-mm
    mm_model_cache_size='1',
    log_level='INFO'
)
# FIXME: Unused, taken from duui-mm, not implemented yet
lru_cache_with_size = lru_cache(maxsize=int(settings.mm_model_cache_size))
initialize_logger(settings.log_level)
logger = get_logger()


def init() -> DUUIEnvironment:
    """
    Initializes the environment for the annotator with all necessary elements.

    :return:
        DUUIEnvironment: The initialized environment for a DUUI component.
    """
    # Sets device for the component
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Logs some general information
    logger.info("TTLab DUUI Multi Modal Embeddings")
    logger.info(f'Name: {settings.annotator_name}')
    logger.info(f'Version: {settings.annotator_version}')
    logger.info(f'Using Device: {device}')

    # Loads the required elements for duui
    lua_communicator = load_lua_communicator()
    type_system = load_typesystem_from_file()

    return DUUIEnvironment(
        communicator=lua_communicator,
        type_system=type_system,
        device=device
    )


environment = init()
app = create_app(settings, environment)
