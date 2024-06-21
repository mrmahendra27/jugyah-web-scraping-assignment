class Config:
    SITE_URL = "https://housing.com"
    PROJECT_PAGE_URL = "/in/buy/projects/mumbai"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.7",
    }
    REQUEST_TIMEOUT = 15
    POOL_CONNECTIONS = 10
    POOL_MAXSIZE = 10


config = Config()
