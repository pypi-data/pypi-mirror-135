import logging

from ruteni.plugins.oauth import oauth

logger = logging.getLogger(__name__)

twitter = oauth.register(
    name="twitter",
    api_base_url="https://api.twitter.com/1.1/",
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authenticate",
)

# TODO: implement…
raise NotImplementedError("FIXME")
