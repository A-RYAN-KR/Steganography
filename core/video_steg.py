"""
Video Steganography Module — Frame-wise LSB Technique.
Hides data across video frames using image LSB on each frame.
Uses OpenCV for frame extraction and reassembly.
"""

import cv2
import numpy as np
import tempfile
import os
import io
from .utils import (
    prepare_payload, extract_payload,
    int_to_binary_32, binary_32_to_int,
    bytes_to_binary, binary_to_bytes
)


def get_video_capacity(video_bytes: bytes) -> int:
    """Calculate maximum bytes that can be hidden in this video."""
    tmp = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    tmp.write(video_bytes)
    tmp.close()
    
    try:
        cap = cv2.VideoCapture(tmp.name)
        total_bits = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            total_bits += frame.flatten().shape[0]
        cap.release()
    finally:
        os.unlink(tmp.name)
    
    available_bits = total_bits - 40
    return available_bits // 8


def encode_in_video(video_bytes: bytes, data: bytes, data_type: str, input_ext: str = '.avi') -> bytes:
    """
    Hide data inside a video using frame-wise LSB steganography.
    
    Args:
        video_bytes: Video file as bytes
        data: Binary data to hide
        data_type: Type of data ('text', 'image', 'audio')
        input_ext: File extension for the input video
    
    Returns:
        Stego video file as bytes (AVI format, lossless)
    """
    # Write to temp file
    tmp_in = tempfile.NamedTemporaryFile(suffix=input_ext, delete=False)
    tmp_in.write(video_bytes)
    tmp_in.close()
    
    tmp_out = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    tmp_out.close()
    
    try:
        cap = cv2.VideoCapture(tmp_in.name)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Use lossless codec for preserving LSB data
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        out = cv2.VideoWriter(tmp_out.name, fourcc, fps, (width, height))
        
        # Prepare payload
        payload = prepare_payload(data, data_type)
        payload_idx = 0
        payload_len = len(payload)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if payload_idx < payload_len:
                flat = frame.flatten()
                bits_to_embed = min(payload_len - payload_idx, len(flat))
                
                for i in range(bits_to_embed):
                    flat[i] = (flat[i] & 0xFE) | int(payload[payload_idx])
                    payload_idx += 1
                
                frame = flat.reshape(frame.shape)
            
            out.write(frame)
        
        cap.release()
        out.release()
        
        if payload_idx < payload_len:
            raise ValueError(
                f"Data too large! Embedded {payload_idx} of {payload_len} bits. "
                "Use a longer or higher-resolution video."
            )
        
        with open(tmp_out.name, 'rb') as f:
            return f.read()
    
    finally:
        os.unlink(tmp_in.name)
        if os.path.exists(tmp_out.name):
            os.unlink(tmp_out.name)


def decode_from_video(video_bytes: bytes):
    """
    Extract hidden data from a stego video.
    
    Returns:
        (data_type, data_bytes) tuple
    """
    tmp = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    tmp.write(video_bytes)
    tmp.close()
    
    try:
        cap = cv2.VideoCapture(tmp.name)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")
        
        # First, extract header from first frame
        all_bits = []
        header_extracted = False
        total_needed = 40  # initial header size
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            flat = frame.flatten()
            for val in flat:
                all_bits.append(str(val & 1))
                if not header_extracted and len(all_bits) == 40:
                    header_str = ''.join(all_bits[:40])
                    type_byte = int(header_str[:8], 2)
                    length = binary_32_to_int(header_str[8:40])
                    total_needed = 40 + length * 8
                    header_extracted = True
                
                if len(all_bits) >= total_needed:
                    break
            
            if len(all_bits) >= total_needed:
                break
        
        cap.release()
        
        if len(all_bits) < total_needed:
            raise ValueError("Invalid stego file or corrupted data.")
        
        binary_str = ''.join(all_bits[:total_needed])
        return extract_payload(binary_str)
    
    finally:
        os.unlink(tmp.name)
