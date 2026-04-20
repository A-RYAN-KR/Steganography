"""
Audio Steganography Module — LSB Technique on WAV samples.
Supports hiding text, image, or audio data inside a WAV audio carrier.
"""

import numpy as np
import wave
import io
import struct
from .utils import prepare_payload, extract_payload, binary_32_to_int


def get_audio_capacity(wav_bytes: bytes) -> int:
    """Calculate maximum bytes that can be hidden in this WAV file."""
    buf = io.BytesIO(wav_bytes)
    with wave.open(buf, 'rb') as wf:
        n_frames = wf.getnframes()
        n_channels = wf.getnchannels()
        total_samples = n_frames * n_channels
    available_bits = total_samples - 40  # subtract header
    return available_bits // 8


def encode_in_audio(wav_bytes: bytes, data: bytes, data_type: str) -> bytes:
    """
    Hide data inside a WAV audio file using LSB steganography.
    
    Args:
        wav_bytes: WAV file as bytes
        data: Binary data to hide
        data_type: Type of data ('text', 'image', 'audio')
    
    Returns:
        Stego WAV file as bytes
    """
    buf_in = io.BytesIO(wav_bytes)
    with wave.open(buf_in, 'rb') as wf:
        params = wf.getparams()
        n_frames = wf.getnframes()
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        raw_data = wf.readframes(n_frames)
    
    # Convert to samples based on sample width
    if sampwidth == 1:
        fmt = f'{len(raw_data)}B'  # unsigned 8-bit
        samples = list(struct.unpack(fmt, raw_data))
    elif sampwidth == 2:
        fmt = f'<{len(raw_data) // 2}h'  # signed 16-bit little-endian
        samples = list(struct.unpack(fmt, raw_data))
    else:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    
    # Prepare payload
    payload = prepare_payload(data, data_type)
    
    if len(payload) > len(samples):
        raise ValueError(
            f"Data too large! Need {len(payload)} bits but carrier "
            f"only has {len(samples)} samples. Use a longer audio file."
        )
    
    # Embed bits using LSB
    for i, bit in enumerate(payload):
        if sampwidth == 1:
            samples[i] = (samples[i] & 0xFE) | int(bit)
        else:  # 16-bit
            if samples[i] >= 0:
                samples[i] = (samples[i] & 0xFFFE) | int(bit)
            else:
                # Handle negative numbers
                samples[i] = (samples[i] | 1) if int(bit) else (samples[i] & ~1)
    
    # Re-pack samples
    if sampwidth == 1:
        new_raw = struct.pack(f'{len(samples)}B', *samples)
    else:
        new_raw = struct.pack(f'<{len(samples)}h', *samples)
    
    # Write output WAV
    buf_out = io.BytesIO()
    with wave.open(buf_out, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(new_raw)
    
    return buf_out.getvalue()


def decode_from_audio(wav_bytes: bytes):
    """
    Extract hidden data from a stego WAV file.
    
    Returns:
        (data_type, data_bytes) tuple
    """
    buf = io.BytesIO(wav_bytes)
    with wave.open(buf, 'rb') as wf:
        n_frames = wf.getnframes()
        sampwidth = wf.getsampwidth()
        raw_data = wf.readframes(n_frames)
    
    # Convert to samples
    if sampwidth == 1:
        fmt = f'{len(raw_data)}B'
        samples = list(struct.unpack(fmt, raw_data))
    elif sampwidth == 2:
        fmt = f'<{len(raw_data) // 2}h'
        samples = list(struct.unpack(fmt, raw_data))
    else:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    
    # Extract header (40 bits)
    header_bits = ''.join(str(abs(s) & 1) for s in samples[:40])
    type_byte = int(header_bits[:8], 2)
    length = binary_32_to_int(header_bits[8:40])
    
    # Validate
    total_needed = 40 + length * 8
    if total_needed > len(samples):
        raise ValueError("Invalid stego file or corrupted data.")
    
    # Extract all bits
    all_bits = ''.join(str(abs(s) & 1) for s in samples[:total_needed])
    
    return extract_payload(all_bits)
