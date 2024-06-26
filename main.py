import pandas as pd
from utils.logger import logger
from scrape.get_all_project_page_urls import get_all_project_page_urls
from scrape.get_project_data import get_project_data
from config import config


def main() -> None:
    links: list = get_all_project_page_urls()

    scraped_projects_data = []
    site_url = config.SITE_URL
    for link in links:
        project_data = get_project_data(site_url, link)
        if project_data:
            scraped_projects_data.append(project_data.model_dump())

    df = pd.DataFrame(scraped_projects_data)
    
    df.to_csv("project_data.csv", index=False)


if __name__ == "__main__":
    main()
