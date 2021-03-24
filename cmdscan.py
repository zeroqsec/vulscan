import argparse
import sys
import time
from config.config import timeout,processCount,delay,concurrency,vulResultPath,pocPath
from scan.scaner import Task
from cores.colors import end, red, white, bad,good, info,yellow,green
from log.log import getLogger

logger = getLogger(__name__)


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='url', dest='target')
parser.add_argument('--data', help='post data', dest='paramData')
parser.add_argument('-e', '--encode', help='encode payloads', dest='encode')
parser.add_argument('--update', help='update',
                    dest='update', action='store_true')
parser.add_argument('--timeout', help='timeout',
                    dest='timeout', type=int, default=timeout)
parser.add_argument('--proxy', help='use prox(y|ies)',
                    dest='proxy', action='store_true')
parser.add_argument('--headers', help='add headers',
                    dest='headers', nargs='?', const=True)
parser.add_argument('--process', help='number of process',
                    dest='processCount', type=int, default=processCount)
parser.add_argument('-c','--coroutineCount',type=int,
                    dest = 'coroutine',help='number of coroutineCount',default=concurrency)
parser.add_argument('-d', '--delay', help='delay between requests',
                    dest='delay', type=int, default=delay)
parser.add_argument('-r','--report',help = 'report of vul scan',default=vulResultPath,dest='reportPath')

args = parser.parse_args()

data = args.paramData
encode = args.encode
update = args.update
timeout = args.timeout
proxy = args.proxy
headers = args.headers
process = args.processCount
coroutines = args.coroutine
delay = args.delay
reportPath = args.reportPath

if update:
    logger.debug("更新")

if args.target == None:
    if args.targets != None:
        targets = args.targets
    else:
        logger.error("%s No parameter of (url|urls)" % bad)
        sys.exit()
else:
    target = args.target
#target = args.target

from scan.scaner import initEnv,processPool
from scan.universal.detect.verify import verifyAllVuls
if __name__ == '__main__':
    print('''%s\tVulScan %sv1.0
                    by hql
                    email:1113732380@qq.com%s''' % (red, green, end))
    time.sleep(1)
    taskid = int(round(time.time()* 1000*1000))
    env = initEnv(
        url = target,
        encoding= encode,
        pocsPath = pocPath,
        output= reportPath,
        headers = headers,
        proxy = proxy,
        taskid = taskid,
        delay = delay,
        coroutineCount = coroutines,
        data = data,
        timeout = timeout,
        processCount = process,
        reportPath = reportPath,
        encode = encode
    )
    processPool(verifyAllVuls,env)
    if env.taskStatus == Task.STOP:
        logger.debug("%s%s Task:{} is over.%s".format(env.taskId) %(good,yellow,end))





