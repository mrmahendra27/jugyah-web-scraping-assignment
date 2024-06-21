from bs4 import BeautifulSoup
from utils.logger import logger
from utils._request import send_request
from config import config


def get_project_urls(page_no: int) -> list:
    try:
        url: str = f"{config.SITE_URL}{config.PROJECT_PAGE_URL}"
        page_url: str = f"{url}?page={page_no}" if page_no else url

        response = send_request(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article")

            if len(articles):
                return [article.find("a").get("href") for article in articles]
            else:
                logger.warn("No Product Link Found!!")
        else:
            logger.error(f"Failed to load the Page, {response.status_code}")

    except Exception as e:
        logger.error(f"Unexpected: {str(e)}")

    return []
