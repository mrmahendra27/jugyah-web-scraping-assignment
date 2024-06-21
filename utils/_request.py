import requests
from config import config
import random


def get_random_user_agent():
    return random.choice(config.USER_AGENTS)


def send_request(url):
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.7",
    }
    response = requests.get(url, timeout=config.REQUEST_TIMEOUT, headers=headers)
    if response.status_code == 403:
        print("403 Forbidden error, changing User-Agent and retrying...")
        headers["User-Agent"] = get_random_user_agent()
        response = requests.get(url, timeout=config.REQUEST_TIMEOUT, headers=headers)
    return response
