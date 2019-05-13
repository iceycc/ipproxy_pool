# -*- coding: utf-8 -*-
import random
import logging
import requests
from ipproxy import IPProxy
from settings import USER_AGENT_LIST,PROXY_CHECK_URLS

# Setting logger output format
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-15s] [%(levelname)8s] [%(name)10s ] - %(message)s (%(filename)s:%(lineno)s)',
                    datefmt='%Y-%m-%d %T'
                    )
logger = logging.getLogger(__name__)


def proxy_to_dict(proxy):
    d = {
        "schema": proxy.schema,
        "ip": proxy.ip,
        "port": proxy.port,
        "used_total": proxy.used_total,
        "success_times": proxy.success_times,
        "continuous_failed": proxy.continuous_failed,
        "created_time": proxy.created_time
    }
    return d


def proxy_from_dict(d):
    return IPProxy(schema=d['schema'], ip=d['ip'], port=d['port'], used_total=d['used_total'],
                   success_times=d['success_times'], created_time=d['created_time'])

# Truncate header and tailer blanks
def strip(data):
    if data is not None:
        return data.strip()
    return data

base_headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def request_page(url, options={}, encoding='utf-8'):
    """send a request,get response

    """
    headers = dict(base_headers, **options)
    if 'User-Agent' not in headers.keys():
        headers['User-Agent']=random.choice(USER_AGENT_LIST)

    logger.info('正在抓取: ' + url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logger.info('抓取成功: ' + url)
            return response.content.decode(encoding=encoding)
    except ConnectionError:
        logger.error('抓取失败' + url)
        return None

def _is_proxy_available(proxy,options={}):
    headers = dict(base_headers, **options)
    if 'User-Agent' not in headers.keys():
        headers['User-Agent'] = random.choice(USER_AGENT_LIST)
    proxies = {proxy.schema:proxy._get_url()}
    check_urls = PROXY_CHECK_URLS[proxy.schema]
    for url in check_urls:
        try:
            response = requests.get(url=url, proxies=proxies, headers=headers,timeout=5)
            if response.status_code == 200:
                logger.info("< "+url+" > 验证代理 < "+proxy._get_url()+" > 结果： 可用  ")
                return True
        except:
            pass
    logger.info("< "+url+" > 验证代理 < "+proxy._get_url()+" > 结果： 不可用  ")
    return False

if __name__ == '__main__':
    headers = dict(base_headers)
    if 'User-Agent' not in headers.keys():
        headers['User-Agent'] = random.choice(USER_AGENT_LIST)
    proxies = {"http":"http://47.94.230.42:9999"}
    response = requests.get("http://www.baidu.com",headers=headers,proxies = proxies,timeout=3)
    print(response.content)
