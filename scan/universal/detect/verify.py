import random
import re

from common.utils import getYamlData
from log.log import getLogger
from cores.requester import requester
from scan.scaner import executeTask,Task
from cores.colors import  red, white, bad, info,run,que,good,green,end
logger = getLogger(__name__)

class Resolver:
    vulname = None
    set = None
    level = None
    description = None
    solution = None
    rules = None
    method = None
    headers = None
    data = None
    allow_redirects = None
    expression = None

def yamlResolver(pocFile):
    resolver = getYamlData(pocFile)
    if 'vulname' in resolver:
        Resolver.vulname = resolver["vulname"]
    if 'expression' in resolver["rules"][0]:
        Resolver.expression = resolver["rules"][0]["expression"]
    if 'method' in resolver["rules"][0]:
        Resolver.method = resolver["rules"][0]["method"]
    if 'level' in resolver:
        Resolver.level = resolver["level"]
    if 'description' in resolver:
        Resolver.description = resolver["description"]
    if 'solution' in resolver:
        Resolver.solution = resolver["solution"]
    if 'set' in resolver:
        Resolver.set = resolver["set"]
    if 'rules' in resolver:
        Resolver.rules = resolver["rules"]
    if 'headers' in resolver["rules"][0]:
        Resolver.headers = resolver["rules"][0]["headers"]
    if 'data' in resolver["rules"][0]:
        Resolver.data = resolver["rules"][0]["data"]
    if 'allow_redirects' in resolver["rules"][0]:
        Resolver.allow_redirects = resolver["rules"][0]["allow_redirects"]

    return Resolver

def randomInt(a,b):
    return random.randint(a,b)

def randomStr(n):
    return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',n))


def verifyVul(url=None,vulname=None,taskId=None,timeout=5,proxies=None,pocsPath=None,vulResultPath=None,verify=True):
    pocFile = "{}\{}".format(pocsPath,vulname)
    Resolver = yamlResolver(pocFile)
    if Resolver.set is not None:
        for key in Resolver.set.keys():
            Resolver.set[key] = eval(eval("Resolver.set[key]"))

    if Resolver.data is not None:
        for key in Resolver.set.keys():
            Resolver.data = re.sub(r'{{'+key+'}}',Resolver.set[key],Resolver.data)
            Resolver.expression = re.sub(r'{{'+key+'}}',Resolver.set[key],Resolver.expression)

        Resolver.data = Resolver.data.replace("{", "").replace("}", "").lstrip()

    response = requester(
        url,
        method = Resolver.method,
        data= Resolver.data,
        headers= Resolver.headers,
        timeout= timeout,
        proxies= proxies,
        verify= verify,
        allow_redirects= Resolver.allow_redirects
    )
    resultSavaPath = "{}\{}.txt".format(vulResultPath, taskId)
    if response is not None:
        if eval(Resolver.expression):
            logger.debug("%s%s任务:{},{} 存在:{},风险:{}%s".format(taskId,url,Resolver.vulname,Resolver.level) %(good,green,end))

            with open(resultSavaPath,mode='a',encoding='utf-8') as f:
                f.write("任务:{},{} 存在:{},风险:{}\n".format(taskId,url,Resolver.vulname,Resolver.level))

@executeTask
async def verifyAllVuls(env):
    try:
        poc = env.pocs.get(block=False,timeout=env.timeout)
        # verifyVul("https://www.shentoushi.top/",poc,env.taskId,env.timeout,
        #     env.proxies,env.pocsPath,env.reportPath)
        verifyVul(env.url, poc, env.taskId, env.timeout,
                  env.proxies, env.pocsPath, env.reportPath)
    except Exception:
        env.taskStatus = Task.STOP


