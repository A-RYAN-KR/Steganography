"""
AES Encryption/Decryption Module for Steganography System.
Uses AES-256 in CBC mode with PKCS7 padding.
"""

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def derive_key(password: str) -> bytes:
    """Derive a 256-bit key from a password using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypt binary data using AES-256-CBC.
    Returns: IV (16 bytes) + ciphertext
    """
    key = derive_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(data, AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext


def decrypt_data(encrypted: bytes, password: str) -> bytes:
    """
    Decrypt AES-256-CBC encrypted data.
    Expects: IV (16 bytes) + ciphertext
    """
    key = derive_key(password)
    iv = encrypted[:16]
    ciphertext = encrypted[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)
    return unpad(padded, AES.block_size)
