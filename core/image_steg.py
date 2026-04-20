"""
Image Steganography Module — LSB (Least Significant Bit) Technique.
Supports hiding text, image, or audio data inside an image carrier.
"""

import numpy as np
from PIL import Image
import io
from .utils import prepare_payload, extract_payload, int_to_binary_32, binary_32_to_int


def get_image_capacity(carrier: Image.Image) -> int:
    """Calculate maximum bytes that can be hidden in this image."""
    img = carrier.convert("RGB")
    total_pixels = img.size[0] * img.size[1]
    # 3 channels per pixel, 1 bit per channel
    total_bits = total_pixels * 3
    # Subtract header bits (8 type + 32 length)
    available_bits = total_bits - 40
    return available_bits // 8


def encode_in_image(carrier: Image.Image, data: bytes, data_type: str) -> Image.Image:
    """
    Hide data inside an image using LSB steganography.
    
    Args:
        carrier: PIL Image to use as carrier
        data: Binary data to hide
        data_type: Type of data ('text', 'image', 'audio')
    
    Returns:
        PIL Image with hidden data (stego image)
    """
    img = carrier.convert("RGB")
    pixels = np.array(img, dtype=np.uint8)
    flat = pixels.flatten()
    
    # Prepare payload with header
    payload = prepare_payload(data, data_type)
    
    if len(payload) > len(flat):
        raise ValueError(
            f"Data too large! Need {len(payload)} bits but carrier "
            f"only has {len(flat)} available. Use a larger carrier image."
        )
    
    # Embed bits using LSB
    for i, bit in enumerate(payload):
        flat[i] = (flat[i] & 0xFE) | int(bit)
    
    # Reshape and return
    stego = flat.reshape(pixels.shape)
    return Image.fromarray(stego, "RGB")


def decode_from_image(stego: Image.Image):
    """
    Extract hidden data from a stego image.
    
    Returns:
        (data_type, data_bytes) tuple
    """
    img = stego.convert("RGB")
    pixels = np.array(img, dtype=np.uint8)
    flat = pixels.flatten()
    
    # Extract header first (40 bits: 8 type + 32 length)
    header_bits = ''.join(str(b & 1) for b in flat[:40])
    type_byte = int(header_bits[:8], 2)
    length = binary_32_to_int(header_bits[8:40])
    
    # Validate length
    total_needed = 40 + length * 8
    if total_needed > len(flat):
        raise ValueError("Invalid stego file or corrupted data.")
    
    # Extract all bits
    all_bits = ''.join(str(b & 1) for b in flat[:total_needed])
    
    return extract_payload(all_bits)
