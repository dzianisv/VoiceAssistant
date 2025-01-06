from contextlib import contextmanager
import os

@contextmanager
def proxy(proxy_url: str):
    http_proxy, https_proxy = os.environ.get('HTTP_PROXY', ''), os.environ.get('HTTPS_PROXY', '')
    os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = proxy_url, proxy_url
    yield
    os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = http_proxy, https_proxy

