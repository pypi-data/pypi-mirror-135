class FrameDecodeError(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


class HandshakeFailureError(Exception):
    pass
