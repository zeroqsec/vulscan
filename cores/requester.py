import requests
import random

from common.utils import isJson
from log.log import getLogger

logger = getLogger(__name__)

def requester(
            url,
            method = None ,
            data = None,
            headers = None,
            timeout = None,
            proxies = None,
            verify = True,
            allow_redirects = True
    ) -> object:
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']

    if headers is None:
        headers = {}
        headers['User-Agent'] = random.choice(user_agents)

    if timeout is None:
        timeout = 5

    try:
        if method == 'GET':
            response = requests.get(url,headers=headers,timeout=timeout,params=data,
                         proxies=proxies,verify=verify,allow_redirects=allow_redirects)
        elif method == 'POST':
            response = requests.post(url,data=data,headers=headers,timeout=timeout,
                          proxies=proxies,verify=verify,allow_redirects=allow_redirects)
        elif method == 'HEAD':
            response = requests.head(url, params=data, headers=headers, timeout=timeout,
                                     proxies=proxies, verify=verify, allow_redirects=allow_redirects)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, timeout=timeout,
                                     proxies=proxies, verify=verify, allow_redirects=allow_redirects)
        elif method == 'PATCH':
            response = requests.patch(url, data=data, headers=headers, timeout=timeout,
                                    proxies=proxies, verify=verify, allow_redirects=allow_redirects)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, timeout=timeout,
                                      proxies=proxies, verify=verify, allow_redirects=allow_redirects)
    except Exception as e:
        logger.error(e)

    return response
