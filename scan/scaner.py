import asyncio
import time
import os
from functools import wraps
from multiprocessing import Pool,Manager,Value

from log.log import getLogger
from common.utils import urlHead
from cores.generate import fileLoadPaylaod
from config.config import processCount,concurrency,xssPayloadPath,vulResultPath
from cores.colors import  red, white, bad, info,run,que,good
from cores.generate import getPathFiles
logger = getLogger(__name__)


class Task:
    START = 2
    STOP  = -1
    PAUSE = 0
    CONTINUE = 1

class Env:
    def __init__(self):
        self.url = None
        self.urls = None
        self.method = None
        self.encoding = None
        self.vulname = None
        self.payloadPath = None
        self.reportPath = None
        self.payloads = None
        self.taskStatus = Value("i",200)
        self.taskId = None
        self.pocs = None
        self.kwargs = None
        self.headers = None
        self.proxy = None


def executeTask(f):
    '''
    execute coroutines
    :param env: init env
    :return:
    '''
    @wraps(f)
    def decorated(env):
        async def main():
            tasks = [f(env) for i in range(concurrency)]
            await asyncio.gather(*tasks)
        asyncio.run(main())
    return decorated

def processPool(fun,env):
    '''
    execute processes
    :param func: coroutine function
    :param env: running env
    :return:
    '''
    pool = Pool(processes=processCount)
    logger.debug("%s start {} processes already.".format(processCount) % good)
    time.sleep(1)
    for i in range(processCount):
        pool.apply_async(func=fun(env))
    pool.close()
    pool.join()


def initEnv(url=None,urls=None,headers=None,proxy=None,taskid=None,method=None,encoding=None,vulname=None,payloads=None
            ,pocsPath=None,payloadPath=None,output=vulResultPath,**kwargs):
    env = Env()
    manager = Manager()
    if vulname is not None:
        logger.debug("%s {} environment is in process of initialization".format(vulname) % run)
    if url is not None:
        logger.debug("%s {} vul test url:{}".format(vulname,urlHead(url,**kwargs)) % good)
    elif urls is not None:
        env.urls = manager.Queue()
        env.urls = urls
        logger.debug("%s {} vul test urls:{} is loading.".format(vulname, os.path.basename(urls)) % good)
    if payloads is not None:
        logger.debug("%s {} paylaods load path:{}".format(vulname,payloadPath) % good)
        try:
            payloadsQ = manager.Queue()
            payloads = fileLoadPaylaod(payloadPath)
            for p in payloads:
                payloadsQ.put(p)
            env.payloads = payloadsQ
        except ValueError:
            logger.error("%s queue is close" % bad)
        logger.debug("%s {} payloads is loading.".format(vulname) % good)
        time.sleep(1)
    if pocsPath is not None:
        env.pocs = manager.Queue()
        env.pocs = getPathFiles(pocsPath)
        logger.debug("%s path:{},pocs is loading.".format(pocsPath) %good)
    env.url = urlHead(url,**kwargs)
    env.urls = urls
    env.method = method
    env.headers = headers
    env.proxy = proxy
    env.encoding = encoding
    env.vulname = vulname
    env.payloadPath = payloadPath
    env.reportPath = output
    # task status set start
    env.taskStatus.value = Task.START
    env.taskId = taskid
    env.kwargs = kwargs
    logger.debug("%s {} initialization of the environment is completed".format(vulname) % good)

    return env


def xssScanApi(**kwargs):
    env = initEnv(**kwargs)
    from scan.plugins.xss import xssScan
    processPool(xssScan,env)

def sqlScanApi(**kwargs):
    env = initEnv(**kwargs)
    from scan.plugins.sql import sqlScan
    processPool(sqlScan,env)

def universScanApi(**kwargs):
    env = initEnv(**kwargs)
    from scan.universal.detect.verify import verifyVul
    processPool(verifyVul,env)


