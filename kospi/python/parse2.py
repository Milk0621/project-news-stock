from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#뉴스 div에서 안의 텍스트만 가져오기(SBS)
driver = webdriver.Chrome()
url = "https://news.sbs.co.kr/news/endPage.do?news_id=N1008065199&plink=ORI&cooper=NAVER"

driver.get(url)

time.sleep(2)

div = driver.find_element(By.CSS_SELECTOR, "#container > div.w_inner > div.w_article > div.w_article_cont > div.w_article_left > div.article_cont_area > div.main_text > div")

inner_html = div.get_attribute("innerHTML")

#bs를 이용해 html파싱
soup = BeautifulSoup(inner_html, "html.parser")

#태그에서 직계자손만 검색
for child in soup.find_all(recursive=False):
    #직계자손 html에서 삭제
    child.decompose()

pure_text = soup.get_text(strip=True)
print(pure_text)