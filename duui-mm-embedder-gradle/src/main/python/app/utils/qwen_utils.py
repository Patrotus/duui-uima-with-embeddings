from typing import Dict, List, Any


def generate_message_for_type(content_type: str, src: str) -> List[Dict[str, Any]]:
    """
    Generates a simple qwen message for a type with src (audio|video|image)
    :param content_type: Type of the content in src (audio|video|image)
    :param src: Source of the data. Can be a Base64 encoded url or a regular url
    :return: Message format expected by qwen
    """
    if content_type == 'image':
        return [
            dict(role='user', content=[
                dict(type='image', image=src),
            ])
        ]
    elif content_type == 'video':
        return [
            dict(role='user', content=[
                # TODO: Where to get those parameters from
                dict(type='video', video=src, fps=1.0, max_pixels=360*420),
            ])
        ]
    # elif content_type == 'audio':
    #     # Use audio_url format for audio (similar to video)
    #     return [
    #         dict(role='user', content=[
    #             dict(type='audio_url', audio_url=dict(url=src)),
    #         ])
    #     ]

    else:
        # Fallback for unknown types
        return [
            dict(role='user', content=[
                dict(type=content_type, image=src),
            ])
        ]
