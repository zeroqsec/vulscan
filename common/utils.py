def is_json(myjson:str) ->bool:
    '''
    judge type of json
    :param myjson:str
    :return:bool
    '''
    import json
    try:
        json.loads(myjson)
    except Exception:
        return False
    return True


