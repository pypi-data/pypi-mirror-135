import email.message
import logging
from typing import Union

from aiosmtplib import SMTP
from aiosmtplib.errors import (
    SMTPConnectError,
    SMTPConnectTimeoutError,
    SMTPResponseException,
    SMTPServerDisconnected,
    SMTPTimeoutError,
)

logger = logging.getLogger(__name__)

Message = Union[email.message.EmailMessage, email.message.Message]


async def send_mail(
    message: Message, hostname: str, port: int = 25, timeout: int = 10
) -> bool:
    smtp = SMTP(hostname=hostname, port=port, timeout=timeout)
    try:
        logger.debug(f"connecting to {hostname}")
        await smtp.connect()
        logger.debug("connected; sending message")
        try:
            await smtp.send_message(message)
            logger.debug("message sent")
        finally:
            smtp.close()
            logger.debug("connection closed")
    except (
        SMTPConnectError,
        SMTPConnectTimeoutError,
        SMTPResponseException,
        SMTPServerDisconnected,
        SMTPTimeoutError,
    ) as exc:
        logger.error(exc)
        return False
    else:
        return True
