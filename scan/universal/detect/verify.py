from config.config import pocPath
from common.utils import getYamlData
from log.log import getLogger
from cores.colors import  red, white, bad, info,run,que,good
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
    allow_rediretcs = None
    expression = None

def yamlResolver(pocFile):
    resolver = getYamlData(pocFile)
    if 'vulname' in resolver:
        Resolver.vulname = resolver["vulname"]
    if 'expression' in resolver:
        Resolver.expression = resolver["expression"]
    if 'method' in resolver["rules"]:
        Resolver.method = resolver["rules"]["method"]
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
    if 'headers' in resolver["rules"]:
        Resolver.headers = resolver["rules"]["headers"]
    if 'data' in resolver["rules"]:
        Resolver.data = resolver["rules"]["data"]
    if 'allow_rediretcs' in resolver["rules"]:
        Resolver.allow_rediretcs = resolver["rules"]["allow_rediretcs"]

    return Resolver




def verifyVul(url,vulname):
    pass



if __name__ == '__main__':
    pass