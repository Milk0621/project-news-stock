from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import re
import pandas as pd

chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.02.01&de=2025.02.01")

dates = datetime.datetime(2025, 2, 1)

news_data=[]
for news in range(0, 3):
    month = dates.strftime("%m")
    day = dates.strftime("%d")

    driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.{month}.{day}&de=2025.{month}.{day}")

    time.sleep(2)
    boxs = None
    height = driver.execute_script("return document.body.scrollHeight")
    while True:
        boxs = driver.find_element(By.CLASS_NAME, "list_news").find_elements(By.CLASS_NAME, "bx")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        count = len(boxs)
        if count >= 20:
            break
        elif height == new_height:
            break
        height = new_height
 
    print(count)

    for i, _ in enumerate(boxs):
        time.sleep(2)
        #print(boxs[i].get_attribute("innerHTML"))
        link = boxs[i].find_element(By.CLASS_NAME, "news_tit").get_attribute("href")
        time.sleep(2)
        driver.execute_script(f"window.open('{link}', '_blank')")
        time.sleep(1)

        #새 탭으로 전환
        driver.switch_to.window(driver.window_handles[1])
        #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
        time.sleep(2)

        try:
            #제목
            title = driver.find_element(By.TAG_NAME, "h1").text
            #본문
            article = driver.find_element(By.TAG_NAME, "article").text
            print(title, article)
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
        except:
            continue
        
        name = boxs[i].find_element(By.CLASS_NAME, "info_group").find_element(By.TAG_NAME, "a").text
        
        dict = {
            "name" : name,
            "title" : title,
            "link" : link,
            "date" : dates,
            "content" : article
        }
        news_data.append(dict)
        print(f"{news}의 {i}번째 저장!")

    dates = dates + datetime.timedelta(days=1)

    print(day)

df = pd.DataFrame(news_data)
df.to_csv("./news_data.csv", index=True)

driver.quit()