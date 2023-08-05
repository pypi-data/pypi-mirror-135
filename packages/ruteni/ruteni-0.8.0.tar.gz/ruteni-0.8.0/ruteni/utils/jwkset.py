import logging
import os
import re
from datetime import datetime
from typing import Any

from anyio import open_file
from jwcrypto.common import json_decode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK, InvalidJWKValue, JWKSet
from jwcrypto.jwt import JWT

logger = logging.getLogger(__name__)

Claims = dict[str, Any]


class KeySet:
    def __init__(self) -> None:
        self.keyset: JWKSet = None
        self.key: JWK = None

    async def load(self, key_file: str) -> None:
        async with await open_file(key_file) as f:
            content = await f.read()

        self.keyset = JWKSet.from_json(content)

        if len(self.keyset) == 0:
            raise Exception("empty key file")

        for key in self.keyset:
            if self.key is None or self.key.get("kid") < key.get("kid"):
                self.key = key

        logger.debug(f"using key {self.key.get('kid')}")

    def create_token(self, **claims: Claims) -> str:
        header = dict(alg="RS256", typ="JWT", kid=self.key.get("kid"))
        jwt = JWT(header=header, claims=claims)
        jwt.make_signed_token(self.key)
        return jwt.serialize()

    def get_claims(self, token: str) -> Claims:
        jwt = JWT(jwt=token, key=self.keyset)
        return json_decode(jwt.claims)

    def export(self) -> str:
        return self.keyset.export(private_keys=False)


class KeyCollection:
    def __init__(self, key_dir: str, create: bool = False) -> None:

        self.key_dir = key_dir
        self.keys = []

        if not os.path.exists(key_dir):
            if create:
                os.mkdir(self.key_dir)
            else:
                raise Exception(f"key dir {key_dir} does not exist")

        if not os.path.isdir(key_dir):
            logger.error(f"{key_dir} is not a directory")
            return

        for filename in sorted(os.listdir(key_dir)):

            m = re.match(r"(\d+)(?:-(\d+))?", filename)
            if not m:
                logger.error(f"ignoring {filename}")
                continue

            created = datetime.fromtimestamp(int(m.group(1)))
            revoked = datetime.fromtimestamp(int(m.group(2))) if m.group(2) else None

            file_path = os.path.join(key_dir, filename)
            with open(file_path) as f:
                content = f.read()

            try:
                key = JWK.from_json(content)
            except InvalidJWKValue:
                logger.error(f"{file_path} is an invalid key file")
            else:
                try:
                    kid = int(key.get("kid"))
                except ValueError:
                    logger.error(f"{file_path} has an invalid key id")
                else:
                    self.keys.append([filename, key, created, revoked])
                    if revoked:
                        logger.debug(f"key {kid} revoked")

    def generate(self, kty: str = "RSA", size: int = 2048) -> None:
        current_kid = -1
        for filename, key, created, revoked in self.keys:
            kid = int(key.get("kid"))
            if current_kid < kid:
                current_kid = kid
        logger.debug(f"current kid: {current_kid}")

        key = JWK.generate(kty=kty, size=size, kid=str(current_kid + 1))
        content = key.export()

        created = int(datetime.now().timestamp())
        filename = f"{created}.json"
        file_path = os.path.join(self.key_dir, filename)

        with open(file_path, "w") as f:
            f.write(content)

        logger.debug(f"new key file: {file_path}")
        self.keys.append([filename, key, created, None])

    def revoke(self, kid: int) -> None:
        for filename, key, created, revoked in self.keys:
            if kid == key.get("kid"):
                if not revoked:
                    revoked = int(datetime.now().timestamp())
                    print("mv", filename, filename[:-5] + "-" + str(revoked) + ".json")
                else:
                    logger.error(f"{kid} already revoked")
                break

    def as_jwkset(self) -> JWKSet:
        jwkset = JWKSet()
        for filename, key, created, revoked in self.keys:
            if not revoked:
                jwkset.add(key)
        return jwkset

    def export(self, public_json: str, private_json: str) -> None:
        jwkset = self.as_jwkset()

        private_dir = os.path.dirname(private_json)
        if private_dir != "":
            os.makedirs(private_dir, exist_ok=True)

        with open(private_json, "w") as f:
            f.write(jwkset.export(private_keys=True))

        public_dir = os.path.dirname(public_json)
        if public_dir != "":
            os.makedirs(public_dir, exist_ok=True)

        with open(public_json, "w") as f:
            f.write(jwkset.export(private_keys=False))

    def print(self) -> None:
        from tabulate import tabulate

        print(
            tabulate(
                tuple(
                    (filename, key.get("kid"), created, revoked)
                    for filename, key, created, revoked in self.keys
                ),
                headers=("filename", "kid", "created", "revoked"),
            )
        )

    def encrypt(self, payload: str, kid: int) -> str:
        if kid:
            for filename, key, created, revoked in self.keys:
                if int(key.get("kid")) == kid:
                    if revoked:
                        raise Exception(f"key {kid} is revoked")
                    break
            else:
                raise Exception(f"unknown key {kid}")
        else:
            latest_key = None
            for filename, key, created, revoked in self.keys:
                if not revoked and (
                    latest_key is None
                    or int(key.get("kid")) > int(latest_key.get("kid"))
                ):
                    latest_key = key
            if latest_key is None:
                raise Exception("empty keyset")
            key = latest_key

        # logger.debug(f'using key {key.get('kid')}')

        public_key = JWK()
        public_key.import_key(**json_decode(key.export_public()))

        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A256CBC-HS512",
            "typ": "JWE",
            "kid": key.get("kid"),
        }

        jwe = JWE(
            payload.encode("utf-8"),
            recipient=public_key,
            protected=protected_header,
        )
        return jwe.serialize()


if __name__ == "__main__":

    from argparse import ArgumentParser, Namespace

    parser = ArgumentParser(prog="jwkset")
    parser.add_argument("--key-dir", default=".")
    subparsers = parser.add_subparsers(help="sub-command help")

    def do_new(args: Namespace) -> None:
        collection = KeyCollection(args.key_dir, True)
        collection.generate()

    parser_new = subparsers.add_parser("new")
    parser_new.set_defaults(func=do_new)

    def do_list(args: Namespace) -> None:
        collection = KeyCollection(args.key_dir)
        collection.print()

    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=do_list)

    def do_revoke(args: Namespace) -> None:
        collection = KeyCollection(args.key_dir)
        collection.revoke(args.kid)

    parser_revoke = subparsers.add_parser("revoke")
    parser_revoke.add_argument("kid")
    parser_revoke.set_defaults(func=do_revoke)

    def do_export(args: Namespace) -> None:
        collection = KeyCollection(args.key_dir)
        collection.export(args.public_keys, args.private_keys)

    parser_export = subparsers.add_parser("export")
    parser_export.add_argument("--public-keys", default="public-keys.json")
    parser_export.add_argument("--private-keys", default="private-keys.json")
    parser_export.set_defaults(func=do_export)

    def do_encrypt(args: Namespace) -> None:
        collection = KeyCollection(args.key_dir)
        print(collection.encrypt(args.data, args.kid))

    parser_encrypt = subparsers.add_parser("encrypt")
    parser_encrypt.add_argument("-k", "--kid", type=int, default=None)
    parser_encrypt.add_argument("data")
    parser_encrypt.set_defaults(func=do_encrypt)

    args = parser.parse_args()
    args.func(args)
