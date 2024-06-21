import requests
from config import config


def create_session_with_pool():
    session = requests.Session()

    adapter = requests.adapters.HTTPAdapter(
        pool_connections=config.POOL_CONNECTIONS, pool_maxsize=config.POOL_MAXSIZE
    )
    session.adapters["http://"] = adapter
    session.adapters["https://"] = adapter

    session.timeout = config.REQUEST_TIMEOUT
    
    if config.HEADERS:
        session.headers.update(config.HEADERS)

    
    return session


def send_request(url):
    session = create_session_with_pool()
    response = session.get(url)
    return response
