import asyncio
import time
import os
from functools import wraps
from multiprocessing import Pool,Manager,Value

from log.log import getLogger
from common.utils import urlHead
from cores.generate import fileLoadPaylaod
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
        self.timeout = None
        self.headers = None
        self.proxies = None
        self.process = None
        self.coroutines = None
        self.pocsPath = None


def executeTask(f):
    '''
    execute coroutines
    :param env: init env
    :return:
    '''
    @wraps(f)
    def decorated(env):
        async def main():
            tasks = [f(env) for i in range(env.coroutines)]
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
    pool = Pool(processes=env.process)
    logger.debug("%s Start {} processes already.".format(env.process) % good)
    time.sleep(1)
    for i in range(env.process):
        pool.apply_async(func=fun(env))
    pool.close()
    pool.join()


def initEnv(url=None,urls=None,taskid=None,method=None,encoding=None,vulname=None,payloads=None
            ,pocsPath=None,proxy=None,timeout=None,payloadPath=None,output=None,processCount=None,coroutineCount=None,**kwargs):
    env = Env()
    manager = Manager()
    if vulname is not None:
        logger.debug("%s environment is in process of initialization" % run)
    if url is not None:
        logger.debug("%s Vul test url:{}".format(urlHead(url,**kwargs)) % good)
    if payloads is not None:
        logger.debug("%s Paylaods load path:{}".format(payloadPath) % good)
        try:
            payloadsQ = manager.Queue()
            payloads = fileLoadPaylaod(payloadPath)
            for p in payloads:
                payloadsQ.put(p)
            env.payloads = payloadsQ
        except ValueError:
            logger.error("%s Queue is close" % bad)
        logger.debug("%s {} payloads is loading.".format(vulname) % good)
        time.sleep(1)
    if pocsPath is not None:
        env.pocs = Manager().Queue()
        pocsList = getPathFiles(pocsPath)
        while len(pocsList) != 0:
            env.pocs.put(pocsList.pop())
        logger.debug("%s Path:{},pocs is loading.".format(pocsPath) %good)

    env.url = urlHead(url,**kwargs) if url is not None else url
    env.urls = urls
    env.method = method
    env.encoding = encoding
    env.vulname = vulname
    env.payloadPath = payloadPath
    env.reportPath = output
    # task status set start
    env.taskStatus.value = Task.START
    env.taskId = taskid
    env.proxies = proxy
    env.process = processCount
    env.coroutines = coroutineCount
    env.timeout = timeout
    env.pocsPath = pocsPath
    env.kwargs = kwargs
    logger.debug("%s Initialization of the environment is completed" % good)

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


