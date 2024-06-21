from scrape.get_project_urls import get_project_urls


def get_all_project_page_urls() -> list:
    page_no: int = 1
    project_detail_page_urls: list = []

    while len(project_detail_page_urls) <= 100:
        project_detail_page_urls.extend(get_project_urls(page_no))
        page_no += 1

    return project_detail_page_urls
