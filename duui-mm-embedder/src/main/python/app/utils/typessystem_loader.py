from cassis import load_typesystem, TypeSystem

from app.constants import TYPESYSTEM_FILE_NAME
from app.logger import get_logger


def load_typesystem_from_file() -> TypeSystem:
    """
    Loads the typesystem from a given file
    :return: The typesystem as a TypeSystem type from cassis
    """
    logger = get_logger()

    logger.debug(f'Loading type system from {TYPESYSTEM_FILE_NAME}')
    with open(TYPESYSTEM_FILE_NAME, 'rb') as type_file:
        type_system = load_typesystem(type_file)
        return type_system
