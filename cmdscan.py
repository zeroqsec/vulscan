import argparse
import sys
from config.config import timeout,processCount,delay,concurrency,vulResultPath,pocPath
from cores.colors import end, red, white, bad, info,yellow,green
from log.log import getLogger

logger = getLogger(__name__)

print('''%s\tVulScan %sv1.0
%s''' % (red, white, end))

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='url', dest='target')
parser.add_argument('--urls', help='urls', dest='targets')
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
parser.add_argument('-t', '--process', help='number of process',
                    dest='processCount', type=int, default=processCount)
parser.add_argument('-c','--coroutineCount',type=int,
                    dest = 'coroutine',help='number of coroutineCount',default=concurrency)
parser.add_argument('-d', '--delay', help='delay between requests',
                    dest='delay', type=int, default=delay)
parser.add_argument('-r','--report',help = 'report of vul scan',default=vulResultPath,dest='reportPath')

args = parser.parse_args()
print(args)

data = args.paramData
encode = args.encode
update = args.update
timeout = args.timeout
proxy = args.proxy
headers = args.headers
process = args.processCount
coroutine = args.coroutine
delay = args.delay
reportPath = args.reportPath


if args.target == None:
    if args.targets != None:
        targets = args.targets
    else:
        logger.debug("%s No parameter of (url|urls)" % bad)
        #sys.exit()
else:
    target = args.target

try:
    target
except NameError as e:
    target = None
try:
    targets
except NameError as e:
    targets = None

import time
from scan.scaner import xssScanApi,sqlScanApi,universScanApi,initEnv
from scan.universal.detect.verify import verifyVul
if __name__ == '__main__':
    taskid = lambda : int(round(time.time()* 1000*1000))
    env = initEnv(
        url = target,
        urls = targets,
        encoding= encode,
        pocs = pocPath,
        output= reportPath,
        headers = headers,
        proxy = proxy,
        taskid = taskid
    )




