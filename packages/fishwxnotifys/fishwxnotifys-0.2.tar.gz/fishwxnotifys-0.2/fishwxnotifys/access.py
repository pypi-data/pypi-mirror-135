import requests

from django.core.cache import cache
from django.conf import settings

from fishwxnotifys.config import GET_ACCESS_TOEN_URL
from fishwxnotifys.exceptions import WxAuthError


APPID = settings.APPID
APP_SECRET = settings.APP_SECRET
CACHE_KEY_ACCESS_TOKEN = "wxnotify_access_token"

def _access_token():
    response = requests.get(
        GET_ACCESS_TOEN_URL.format(APPID=APPID,APPSECRET=APP_SECRET)
    )
    if response.json()["errcode"] == 40164:
        raise WxAuthError("无效的请求来源ip,detail={e}".format(e=response.json()["errmsg"]))
    cache.set(
        "access_token", response.json()["access_token"], response.json()["expires_in"]
    )


def get_access_token():
    token = cache.get(CACHE_KEY_ACCESS_TOKEN)
    if not token:
        _access_token()
        token = cache.get(CACHE_KEY_ACCESS_TOKEN)
        return token
    else:
        return token
