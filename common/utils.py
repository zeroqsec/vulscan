import requests
import json
import re
import os
import base64 as b64
import yaml

def isJson(myjson:str) ->bool:
    '''
    judge type of json.
    :param myjson:data that the type of json,type<str>
    :return:bool
    '''
    try:
        json.loads(myjson)
    except Exception:
        return False
    return True

def urlHead(target:str,**kwargs)->str:
    '''
    deal with url and add protocal head,
    if url without http protocal head or https protocal head.
    :param target:url,type:<str>
    :param kwargs:others parameters
    :return:url,type<str>
    '''
    if not target.startswith('http'):
        try:
            requests.get('https://' + target, 'GET',**kwargs)
            target = 'https://' + target
        except:
            target = 'http://' + target
    return target


def getParams(url, data:dict):
    '''
    get url paramter or input paramter by data.
    exp1: https://www.baidu.com/a?id=1
    if url like exp1,will return {'id':'1'}.
    exp2: https://www.baidu.com/a
    if url like exp2,the data parameter such as {'name':'mike'},will return {'name','mike'}.
    if input url like exp1 ,input data parameter at the same time,will return like exp1.
    :param url: type<str>
    :param data: type<dict>
    :return: None or dict
    '''
    params = {}
    if '=' in url:
        data = url.split('?')[1]
    elif data:
        params = data
    else:
        return None
    if not params:
        parts = data.split('&')
        for part in parts:
            each = part.split('=')
            if len(each) < 2:
                each.append('')
            try:
                params[each[0]] = each[1]
            except IndexError:
                params = None
    return params

def base64(string):
    '''
    decode or encode by base64 base on input parameter
    :param string:
    :return:
    '''
    if re.match(r'^[A-Za-z0-9+\/=]+$', string) and (len(string) % 4) == 0:
        return b64.b64decode(string.encode('utf-8')).decode('utf-8')
    else:
        return b64.b64encode(string.encode('utf-8')).decode('utf-8')

def cleanComment(response:str) ->str:
    '''
    clean html comment
    :param response:
    :return: type<str>
    '''
    response = re.sub(r'<!--[.\s\S]*?-->', '', response)
    return response

def extractScripts(response) ->list:
    '''
    extract javascript
    :param response:
    :return:type<list>
    '''
    matches = re.findall(r'(?s)<script.*?>(.*?)</script>', response.lower())
    return matches

def getYamlData(yamlFile):
    '''
    get yaml data.
    :param yamlFile:path
    :return:
    '''
    with open(yamlFile,mode='r',encoding='utf-8') as f:
        return yaml.safe_load(f.read())

def getAllFileNames(path):
    fileNames = []
    for root,dirs,files in os.walk(path):
        for f in files:
            fileNames.append(f)
    return fileNames


if __name__ =='__main__':
    # response = requests.get("https://www.anquanke.com/search?s=aflgwgw")
    # print(extractScripts(response.text))
    from config.config import pocPath
    a= getYamlData('{}/test.yaml'.format(pocPath))
    print(a)
