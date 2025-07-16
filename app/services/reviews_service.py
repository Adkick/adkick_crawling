import urllib.parse
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# (7/7) pcmap URL 기준
# review_sort가 일부 case에서 적용 불가능한 것으로 보여
# 파라미터 적용 임시 비활성화 (최신순 적용)

def reviews_fetch(place_id: str, max_clicks: int) -> str:
    # place_id URI 인코딩
    enc_id = urllib.parse.quote_plus(place_id)
    url = f"https://pcmap.place.naver.com/place/{enc_id}/review/visitor"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.93 Mobile Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)

        # 첫 페이지 스크롤
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

        # '더보기' 버튼 클릭
        # TO-DO: pcmap 기준 셀렉터 변경 필요
        for _ in range(max_clicks):
            try:
                btn = driver.find_element(By.XPATH, '//a[contains(text(),"더보기")]')
                btn.click()
                time.sleep(0.5)
            except:
                break

        time.sleep(1)
        return driver.page_source

    finally:
        driver.quit()


def reviews_parser(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")

    # TO-DO: Specify selector
    # 관련 레퍼런스에는 'EjjAWcontent'를 셀렉터로 잡아야 한다고 하였으나
    # (7/6 기준) 태그명 'EjjAW'로 변경된 것으로 추측됨 (추가 조사 필요)
    items = soup.select("li.place_apply_pui.EjjAW")
    reviews: List[Dict] = []

    for item in items:
        # elements
        nick_el   = item.select_one("div.pui__JiVbY3 > span.pui__uslU0d")
        cont_el   = item.select_one("div.pui__vn15t2 > a")
        date_el   = item.select("div.pui__QKE5Pr > span.pui__gfuUIT > time")
        revisit_el= item.select("div.pui__QKE5Pr > span.pui__gfuUIT")

        reviews.append({
            "nickname": nick_el.get_text(strip=True)   if nick_el   else "",
            "content":  cont_el.get_text(strip=True)   if cont_el   else "",
            "date":     date_el[0].get_text(strip=True) if date_el else "",
            "revisit":  revisit_el[1].get_text(strip=True) if len(revisit_el) > 1 else ""
        })

    return reviews
