from typing import Dict, List, Any


def generate_message_for_type(content_type: str, src: str) -> List[Dict[str, Any]]:
    """
    Generates a simple qwen message for a type with src (audio|video|image)
    :param content_type: Type of the content in src (audio|video|image)
    :param src: Source of the data. Can be a Base64 encoded url or a regular url
    :return: Message format expected by qwen
    """
    return [
        dict(role='user', content=[
            dict(type=f'{content_type}', image=f'{src}'),
        ])
    ]
