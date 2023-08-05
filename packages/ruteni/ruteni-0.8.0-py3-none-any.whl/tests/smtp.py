from ruteni.utils.smtp import Message


class SMTPMock:
    def __init__(self) -> None:
        self.allow_email = True
        self.messages: dict[str, list[Message]] = {}

    def allow_email_delivery(self, allow: bool) -> None:
        self.allow_email = allow

    async def send_mail(self, message: Message, host: str) -> bool:
        if self.allow_email:
            if host not in self.messages:
                self.messages[host] = []
            self.messages[host].append(message)
            return True
        else:
            return False

    def get_email(self, host: str) -> Message:
        return self.messages[host].pop(0)
