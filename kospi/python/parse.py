from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#뉴스들에서 p태그만 가져오기(본문), 연합뉴스
driver = webdriver.Chrome()
url = "https://www.mk.co.kr/news/stock/11292534"

driver.get(url)

time.sleep(2)

div = driver.find_element(By.CLASS_NAME, "news_cnt_detail_wrap")

p_s = div.find_elements(By.CSS_SELECTOR, "p")

p_text = " ".join([p.text.strip() for p in p_s])
print(p_text)