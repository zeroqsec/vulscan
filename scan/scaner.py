import asyncio
import time
from functools import wraps
from multiprocessing import Pool,Manager,Value

from log.log import getLogger
from common.utils import urlHead
from cores.generate import fileLoadPaylaod
from config.config import processCount,concurrency,xssPayloadPath,vulResultPath
from cores.colors import  red, white, bad, info,run,que,good
logger = getLogger(__name__)


class Task:
    START = 2
    STOP  = -1
    PAUSE = 0
    CONTINUE = 1

class Env:
    url = None
    urls = None
    method = None
    encoding = None
    vulname = None
    payloadPath = None
    reportPath = None
    payloads = None
    taskStatus = Value("i",200)
    taskId = None
    kwargs = None



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
    for i in range(processCount):
        pool.apply_async(func=fun(env))
    pool.close()
    pool.join()


def initEnv(url,method,encoding,vulname,payloadPath,output=vulResultPath,**kwargs):
    logger.debug("%s {} environment is in process of initialization".format(vulname) % run)
    time.sleep(1)
    logger.debug("%s {} vul test url:{}".format(vulname,url) % good)
    logger.debug("%s {} paylaods load path:{}".format(vulname,payloadPath) % good)
    output = "{}\\{}Report.txt".format(output,vulname)
    logger.debug("%s {} report output path:{}".format(vulname, output) % good)
    try:
        manager = Manager()
        payloadsQ = manager.Queue()
        payloads = fileLoadPaylaod(payloadPath)
        for p in payloads:
            payloadsQ.put(p)
        time.sleep(1)
    except ValueError:
        logger.error("%s queue is close" % bad)
    logger.debug("%s {} payloads is loading.".format(vulname) % good)
    time.sleep(1)
    Env.url = urlHead(url,**kwargs)
    Env.method = method
    Env.encoding = encoding
    Env.vulname = vulname
    Env.payloadPath = payloadPath
    Env.reportPath = output
    Env.payloads = payloadsQ
    # task status set start
    Env.taskStatus.value = Task.START
    Env.taskId = Value('i',lambda : int(round(time.time()* 1000*1000)))
    Env.kwargs = kwargs
    logger.debug("%s {} initialization of the environment is completed".format(vulname) % good)

    return Env



if __name__ == "__main__":
    Env = initEnv("www.baidu.com",
         "GET",
         "base64",
         "xss",
         xssPayloadPath,
         )
    from scan.plugins.xss import xssscan
    processPool(xssscan,Env)

