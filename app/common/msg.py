# coding: utf-8

code = 'code'
msg = 'msg'
data = 'data'


class Error:
    API_KEY_ERROR = {code: 403, msg: '', data: []}
    LENGTH_ERROR = {code: -5001, msg: '', data: []}
    INVALID_SYMBOL = {code: -5002, msg: '', data: []}
    ASSET_TARGET_NULL = {code: -5003, msg: '', data: []}
    ASSET_TARGET_ERROR = {code: -5004, msg: '', data: []}
    NO_TASK_ID = {code: -5100, msg: '', data: []}


class BaseMSG:
    @classmethod
    def msg(cls, res, **kwargs):
        res.update(kwargs)
        return res


class MSG(BaseMSG):

    @classmethod
    def Success(cls, **kwargs):
        res = {code: ResponseCode.SUCCESS, msg: ResponseMessage.SUCCESS}
        return super().msg(res, **kwargs)

    @classmethod
    def Failed(cls, **kwargs):
        res = {code: ResponseCode.FAILED, msg: ResponseMessage.FAILED}
        return super().msg(res, **kwargs)

    @classmethod
    def ApiKeyNull(cls, **kwargs):
        res = {code: ResponseCode.API_KEY_NULL, msg: ResponseMessage.API_KEY_NULL}
        return super().msg(res, **kwargs)


class ResponseCode(object):
    START = 0  # 成功
    FAILED = -1  # 失败
    SUCCESS = 200
    NO_RESOURCE_FOUND = 40001  # 未找到资源
    INVALID_PARAMETER = 40002  # 参数无效
    ACCOUNT_OR_PASS_WORD_ERR = 40003  # 账户或密码错误
    API_KEY_ERROR = 40004
    API_KEY_NULL = 403
    ASSET_TARGET_ERROR = -50004
    REPORT_URL_NULL = -50005
    INITIAL_STATE = 20010
    FILE_BUILDING = 20011
    FILE_BUILD_FAILED = 50001
    EXTRACTING = 20012
    EXTRACT_FAILED = 50002
    FILE_LOST_INDEX = 50003
    FILE_READING = 20014
    FILE_READ_FAILED = 50004
    ONLY_SUPPORT_AFFECTED_ITEMS_REPORT = 50005
    NO_TASK_ID = -5100
    NO_CTL = -5101
    NO_IP = -5102


class ResponseMessage(object):
    SUCCESS = "成功"
    FAILED = "失败"
    API_KEY_ERROR = '缺失参数{}'
    API_KEY_NULL = '缺少参数'
    NO_RESOURCE_FOUND = "未找到资源"
    INVALID_PARAMETER = "参数无效"
