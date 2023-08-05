class Content:
    def __init__(self, body: bytes, content_type: bytes) -> None:
        self.body = body
        self.content_type = content_type


TEXT_PLAIN_CONTENT_TYPE = b"text/plain; charset=utf-8"
