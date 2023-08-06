from __future__ import annotations

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PUBLIC_EXPONENT = 65537


def generate_ssh_key_pair(bits: int = 2048) -> tuple[str, str]:
    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=PUBLIC_EXPONENT, key_size=bits
    )

    private_key = key.private_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=crypto_serialization.NoEncryption(),
    )

    public_key = key.public_key().public_bytes(
        encoding=crypto_serialization.Encoding.OpenSSH,
        format=crypto_serialization.PublicFormat.OpenSSH,
    )

    return private_key.decode(), public_key.decode()
