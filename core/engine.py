"""
Unified Steganography Engine — orchestrates encoding/decoding across all carrier types.
"""

from PIL import Image
import io
from .crypto import encrypt_data, decrypt_data
from .image_steg import encode_in_image, decode_from_image, get_image_capacity
from .audio_steg import encode_in_audio, decode_from_audio, get_audio_capacity
from .video_steg import encode_in_video, decode_from_video, get_video_capacity
from .utils import image_to_bytes


def encode(data: bytes, data_type: str, carrier_bytes: bytes, carrier_type: str,
           password: str = None, video_ext: str = '.avi') -> bytes:
    if password:
        data = encrypt_data(data, password)

    if carrier_type == 'image':
        carrier_img = Image.open(io.BytesIO(carrier_bytes)).convert("RGB")
        stego_img = encode_in_image(carrier_img, data, data_type)
        buf = io.BytesIO()
        stego_img.save(buf, format='PNG')
        return buf.getvalue()
    elif carrier_type == 'audio':
        return encode_in_audio(carrier_bytes, data, data_type)
    elif carrier_type == 'video':
        return encode_in_video(carrier_bytes, data, data_type, input_ext=video_ext)
    else:
        raise ValueError(f"Unsupported carrier type: {carrier_type}")


def decode(stego_bytes: bytes, carrier_type: str, password: str = None):
    if carrier_type == 'image':
        stego_img = Image.open(io.BytesIO(stego_bytes)).convert("RGB")
        data_type, data = decode_from_image(stego_img)
    elif carrier_type == 'audio':
        data_type, data = decode_from_audio(stego_bytes)
    elif carrier_type == 'video':
        data_type, data = decode_from_video(stego_bytes)
    else:
        raise ValueError(f"Unsupported carrier type: {carrier_type}")

    if password:
        data = decrypt_data(data, password)

    return data_type, data


def check_capacity(carrier_bytes: bytes, carrier_type: str, video_ext: str = '.avi') -> int:
    if carrier_type == 'image':
        img = Image.open(io.BytesIO(carrier_bytes)).convert("RGB")
        return get_image_capacity(img)
    elif carrier_type == 'audio':
        return get_audio_capacity(carrier_bytes)
    elif carrier_type == 'video':
        return get_video_capacity(carrier_bytes)
    return 0
