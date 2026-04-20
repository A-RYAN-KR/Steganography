"""
Utility functions for data conversion between formats.
"""

import struct
import numpy as np
from PIL import Image
import io


def text_to_binary(text: str) -> str:
    """Convert text string to binary representation."""
    return ''.join(format(b, '08b') for b in text.encode('utf-8'))


def binary_to_text(binary_str: str) -> str:
    """Convert binary string back to text."""
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        if len(byte) == 8:
            chars.append(int(byte, 2))
    return bytes(chars).decode('utf-8', errors='replace')


def bytes_to_binary(data: bytes) -> str:
    """Convert bytes to binary string."""
    return ''.join(format(b, '08b') for b in data)


def binary_to_bytes(binary_str: str) -> bytes:
    """Convert binary string back to bytes."""
    byte_list = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        if len(byte) == 8:
            byte_list.append(int(byte, 2))
    return bytes(byte_list)


def int_to_binary_32(n: int) -> str:
    """Convert integer to 32-bit binary string."""
    return format(n, '032b')


def binary_32_to_int(binary_str: str) -> int:
    """Convert 32-bit binary string to integer."""
    return int(binary_str, 2)


def image_to_bytes(image: Image.Image) -> bytes:
    """Convert PIL Image to bytes (PNG format)."""
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()


def bytes_to_image(data: bytes) -> Image.Image:
    """Convert bytes back to PIL Image."""
    buf = io.BytesIO(data)
    return Image.open(buf)


def prepare_payload(data: bytes, data_type: str) -> str:
    """
    Prepare data payload with header for embedding.
    Header format: [8-bit type][32-bit length][data bits]
    Types: 0x01=text, 0x02=image, 0x03=audio
    """
    type_map = {'text': 0x01, 'image': 0x02, 'audio': 0x03}
    type_byte = format(type_map.get(data_type, 0x01), '08b')
    length_bits = int_to_binary_32(len(data))
    data_bits = bytes_to_binary(data)
    return type_byte + length_bits + data_bits


def extract_payload(binary_str: str):
    """
    Extract data payload from binary string.
    Returns: (data_type, data_bytes)
    """
    type_map = {0x01: 'text', 0x02: 'image', 0x03: 'audio'}
    type_byte = int(binary_str[:8], 2)
    data_type = type_map.get(type_byte, 'text')
    length = binary_32_to_int(binary_str[8:40])
    data_bits = binary_str[40:40 + length * 8]
    data_bytes = binary_to_bytes(data_bits)
    return data_type, data_bytes
