from log.log import getLogger
from scan.scaner import executeTask
from cores.colors import  red, white, bad, info,run,que,good

logger = getLogger(__name__)

@executeTask
async def xssScan(env):
    logger.debug("xss")
    pass
