import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def place_fetcher(query: str, debug: bool = False, timeout: int = 10) -> str:
    pc_ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--user-agent={pc_ua}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        """
    })

    try:
        url = f"https://pcmap.place.naver.com/restaurant/list?query={urllib.parse.quote_plus(query)}"
        driver.get(url)
        driver.implicitly_wait(timeout)
        html = driver.page_source

        if debug:
            start = html.find("RestaurantListSummary")
            end = html.find("}", start) + 1
            return html[start:end] if start != -1 and end != -1 else html

        return html

    finally:
        driver.quit()


def place_parser(html: str) -> str:
    m = re.search(
        r'RestaurantListSummary:[^"]+":\{"__typename":"RestaurantListSummary".+?"id":"(\d+)"',
        html
    )
    if not m:
        raise ValueError("place_id를 HTML에서 찾을 수 없습니다.")
    return m.group(1)
