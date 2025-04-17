from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd

chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(f"https://news.mt.co.kr/mtview.php?no=2025020715304257729")


content = driver.find_element(By.XPATH, "//*[@class='news_body' or @class='article-body' or @id='textBody']")
inner_html = content.get_attribute("innerHTML")

soup = BeautifulSoup(inner_html, "html.parser")

for child in soup.find_all(recursive=False):
    #직계자손 html에서 삭제
    child.decompose()

con_text = soup.get_text(strip=True)
print("@@@@@@@@@@",con_text)


content_box = driver.find_element(By.XPATH, "//*[@class='article' or @class='article_view' or @class='news_cnt_detail_wrap']")
content = content_box.find_elements(By.CSS_SELECTOR, "p")

con_text = " ".join([p.text.strip() for p in content])

print("!!!!!!!!!!!!!!!!",con_text)