import base64
import hashlib
import os

WS_GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


def genmask() -> bytes:
    """Generates a random masking key for a WebSocket frame."""
    return os.urandom(4)


def mask(data: bytes, mask: bytes) -> bytes:
    """Applies a masking key to a byte string.

    Arguments:
        data (bytes): The data to apply the masking key to.

        mask (bytes): The masking key.
    """
    return bytes(data[i] ^ mask[i % 4] for i in range(len(data)))


def genseckey() -> str:
    """Generates a random base64 value for a secret WebSocket key."""
    return base64.b64encode(os.urandom(16)).decode('utf-8')


def genacckey(key: bytes) -> str:
    """Generates an acceept key from a secret WebSocket key.

    Arguments:
        key (str): The secret WebSocket key.
    """
    return base64.b64encode(hashlib.sha1(key + WS_GUID).digest()).decode('utf-8')
