import crypt
import logging
from typing import Union

from asyncssh import SSHServer, SSHServerConnection, SSHServerSession, create_server
from asyncssh.channel import SSHChannel
from ruteni.config import config
from ruteni.services import Service
from starlette.datastructures import State

logger = logging.getLogger(__name__)


# generate host key with: ssh-keygen -f ssh_host_key

SSHD_ADDRESS: str = config.get("RUTENI_SSHD_ADDRESS", default="127.0.0.1")
SSHD_PORT: int = config.get("RUTENI_SSHD_PORT", cast=int, default=2222)
SSHD_SERVER_HOST_KEYS: str = config.get("RUTENI_SSHD_SERVER_HOST_KEYS")


passwords = {"guest": "", "user123": "qV2iEadIGV2rw"}


class MySSHServerSession(SSHServerSession):
    def connection_made(self, channel: SSHChannel) -> None:
        self.channel = channel

    def shell_requested(self) -> bool:
        return True

    def session_started(self) -> None:
        self.channel.write("Welcome\n")

    def data_received(self, data: Union[bytes, str], datatype: int) -> None:
        self.channel.write(data)

    def eof_received(self) -> None:
        self.channel.exit(0)

    def break_received(self, msec: int) -> None:
        self.channel.write("bye\n")
        self.eof_received()


# from paramiko import Channel, PKey, ServerInterface, common
# class Server(ServerInterface):
#     def __init__(self) -> None:
#         pass

#     def check_channel_request(self, kind: str, chanid: int) -> int:
#         # if kind == "session":
#         return common.OPEN_SUCCEEDED

#     def check_auth_publickey(self, username: str, key: PKey) -> int:
#         return common.AUTH_SUCCESSFUL

#     def get_allowed_auths(self, username: str) -> str:
#         return "publickey"

#     def check_channel_exec_request(self, channel: Channel, command: str) -> bool:
#         logger.debug(command)
#         return True


class RuteniSSHServer(SSHServer):
    def connection_made(self, conn: SSHServerConnection) -> None:
        client = conn.get_extra_info("peername")[0]
        logger.debug(f"connection received from {client}")

    def connection_lost(self, exc: BaseException) -> None:
        if exc:
            logger.error(f"connection error: {exc}")
        else:
            logger.debug("connection closed")

    def begin_auth(self, username: str) -> bool:
        return passwords.get(username) != ""

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        pw = passwords.get(username, "*")
        return crypt.crypt(password, pw) == pw

    def session_requested(self) -> SSHServerSession:
        return MySSHServerSession()


class SSHDService(Service):
    def __init__(self) -> None:
        Service.__init__(self, "sshd", 1)

    async def startup(self, state: State) -> None:
        await Service.startup(self, state)
        self.server = await create_server(
            RuteniSSHServer,
            SSHD_ADDRESS,
            SSHD_PORT,
            server_host_keys=SSHD_SERVER_HOST_KEYS,
            # loop=self.deps["core:domain"].loop,
        )

    async def shutdown(self, state: State) -> None:
        await Service.shutdown(self, state)
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None


sshd = SSHDService()
