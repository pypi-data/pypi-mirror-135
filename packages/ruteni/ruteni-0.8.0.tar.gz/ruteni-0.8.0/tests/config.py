import os
import tempfile

from ruteni.config import config
from ruteni.utils.jwkset import KeyCollection

TEST_DIR = tempfile.mkdtemp()
DATABASE_PATH = TEST_DIR + "/test.db"

BASE_URL = "http://localhost:8000"
CLIENT_ID = "client-id"
DOMAIN = "bar.fr"
USER_EMAIL = "username@" + DOMAIN
USER_NAME = "username"
USER_PASSWORD = "lWhgjgjgjHJy765"
USER_LOCALE = "fr-FR"
SITE_NAME = "Ruteni Test"

USER = {
    "id": 2,  # admin is 1
    "display_name": USER_NAME,
    "email": USER_EMAIL,
    "provider": "ruteni",
    "locale": "fr-FR",
    "groups": [],
}

SESSION_SECRET_KEY = "secret-key"
PRIVATE_KEYS = TEST_DIR + "/private_keys.json"
PUBLIC_KEYS = TEST_DIR + "/public_keys.json"
key_collection = KeyCollection(TEST_DIR, True)
key_collection.generate()
key_collection.export(PUBLIC_KEYS, PRIVATE_KEYS)

config.set("RUTENI_ENV", "development")
config.set("RUTENI_JWKEYS_FILE", PRIVATE_KEYS)
config.set("RUTENI_SITE_NAME", SITE_NAME)
config.set("RUTENI_SITE_DOMAIN", "accot.fr")
config.set("RUTENI_VERIFICATION_FROM_ADDRESS", "Bar Baz <bar@baz.fr>")
config.set("RUTENI_SITE_ABUSE_URL", "<abuse_url>")

test_env = {
    "RUTENI_DATABASE_URL": "sqlite:///" + DATABASE_PATH,
    "RUTENI_SESSION_SECRET_KEY": SESSION_SECRET_KEY,
}


def clear_database() -> None:
    os.unlink(DATABASE_PATH)
