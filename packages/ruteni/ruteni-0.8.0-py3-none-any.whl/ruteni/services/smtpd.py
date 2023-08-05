import logging

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP, Envelope, Session
from ruteni.plugins.site import SITE_DOMAIN
from ruteni.services import Service
from starlette.datastructures import State

logger = logging.getLogger(__name__)


class ExampleHandler:
    async def handle_RCPT(
        self,
        server: SMTP,
        session: Session,
        envelope: Envelope,
        address: str,
        rcpt_options: list,
    ) -> str:
        if not address.endswith("@" + SITE_DOMAIN):
            return "550 not relaying to that domain"
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(
        self, server: SMTP, session: Session, envelope: Envelope
    ) -> str:
        logger.debug("Message from %s" % envelope.mail_from)
        logger.debug("Message for %s" % envelope.rcpt_tos)
        if envelope.content:
            logger.debug("Message data:")
            content = (
                envelope.content.decode("utf8", errors="replace")
                if isinstance(envelope.content, bytes)
                else envelope.content
            )
            for ln in content.splitlines():
                logger.debug(f"> {ln}".strip())
        else:
            logger.debug("Message data:EMPTY")
        logger.debug("End of message")
        return "250 Message accepted for delivery"


class SMTPDService(Service):
    def __init__(self) -> None:
        Service.__init__(self, "smtpd", 1)
        self.controller = Controller(ExampleHandler())

    async def startup(self, state: State) -> None:
        await Service.startup(self, state)
        self.controller.start()  # type: ignore

    async def shutdown(self, state: State) -> None:
        await Service.shutdown(self, state)
        self.controller.stop()  # type: ignore


smtpd = SMTPDService()
