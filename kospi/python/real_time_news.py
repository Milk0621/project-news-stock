from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
from datetime import date
import re
import pandas as pd
import pymysql
import schedule


#이데일리, 아시아경제, 매일경제, 한국경제, 머니투데이

today = datetime.datetime.now()
ymd = today.strftime("%Y-%m-%d")
month = today.strftime("%m")
day = today.strftime("%d")


chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#스케줄러
def mail_news():
    conn = pymysql.connect(
        host="158.247.211.92",
        user="milk",
        password="0621",
        database="kospi"
    )
    cursor = conn.cursor()

    driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.{month}.{day}&de=2025.{month}.{day}&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked=1009&nso=so%3Ar%2Cp%3Afrom20250201to20250301&is_sug_officeid=0&office_category=0&service_area=0")
    # 결과 저장할 리스트
    news_data = []

    height = driver.execute_script("return document.body.scrollHeight")
    while True:
        boxs = driver.find_element(By.CLASS_NAME, "list_news").find_elements(By.CLASS_NAME, "bx")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break
        height = new_height

    for i, _ in enumerate(boxs):
        link = boxs[i].find_element(By.CLASS_NAME, "news_tit").get_attribute("href")
        time.sleep(2)
        driver.execute_script(f"window.open('{link}', '_blank')")
        time.sleep(1)

        #새 탭으로 전환
        driver.switch_to.window(driver.window_handles[1])
        #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
        time.sleep(2)
        
        title = driver.title
        thumb = driver.find_element(By.CSS_SELECTOR, "#container > section.contents > div.news_detail_body_group > section > div.min_inner > div.sec_body > div.news_cnt_detail_wrap > div.thumb_area.img > figure > div")
        img = thumb.find_element(By.TAG_NAME, "img").get_attribute("src")
        print(img)
        div = driver.find_element(By.CLASS_NAME, "news_cnt_detail_wrap")
        content = div.find_elements(By.CSS_SELECTOR, "p")
        con_text = " ".join([p.text.strip() for p in content])
        print(title, con_text)
        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        dict = {
            "name" : "매일경제",
            "title" : title,
            "link" : link,
            "content" : con_text,
            "img" : img,
            "date" : ymd
        }
        news_data.append(dict)
        insert_query = "insert into news(name, title, link, content, img, date)values('매일경제', %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (title, link, con_text, img, ymd))
        conn.commit()

    df2 = pd.DataFrame(news_data)
    df2.to_csv(f"./mail-{date.today()}.csv", index=False)
    print("저장!")

    cursor.close()
    conn.close()

mail_news()
# schedule.every(10).minutes.do(mail_news) #10분마다

# while True:
#     if datetime.today().hour == 00 or datetime.today().hour == 0:
#         break

#     schedule.run_pending()
#     time.sleep(2)
