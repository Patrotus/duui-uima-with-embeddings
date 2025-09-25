from app.constants import LUA_COMMUNICATION_SCRIPT_FILENAME, STATIC_ENCODING
from app.logger import get_logger


def load_lua_communicator() -> str:
    """
    Loads the communication script from a specified lua file
    :return: Content of the file as a string
    """
    logger = get_logger()

    logger.debug(f'Loading lua communicator from {LUA_COMMUNICATION_SCRIPT_FILENAME}')
    with open(LUA_COMMUNICATION_SCRIPT_FILENAME, 'rb') as lua_file:
        lua_communication_script = lua_file.read().decode(STATIC_ENCODING)
        logger.debug(f'Lua communication script: {lua_communication_script}')
        return lua_communication_script
