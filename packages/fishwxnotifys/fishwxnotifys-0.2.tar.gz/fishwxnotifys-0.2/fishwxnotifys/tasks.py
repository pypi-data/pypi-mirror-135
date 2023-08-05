import json
import requests

from celery.task import task
from django.conf import settings

from fishwxnotifys.access import get_access_token
from fishwxnotifys.config import TEMPLATE_MSG_URL
from fishwxnotifys.exceptions import SendMsgRequestError

APPID = settings.APPID

@task
def send_message(message:dict):
    message = json.dumps(message)
    _access_token = get_access_token()
    url = TEMPLATE_MSG_URL.format(_access_token)
    try:
        res = requests.post(url, data=message)
    except Exception as e:
        raise SendMsgRequestError("请求模板消息URL失败,detail={e}".format(e=str(e)))
    return res
