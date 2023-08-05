class WxnotifyError(Exception):
    pass

class SendMsgRequestError(WxnotifyError):
    pass

class WxAuthError(WxnotifyError):
    pass