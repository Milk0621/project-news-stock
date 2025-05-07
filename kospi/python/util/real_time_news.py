from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymysql
import schedule
from bs4 import BeautifulSoup
import time
import datetime
from datetime import date
import re
import subprocess
from pymysql.converters import escape_string
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ML.kobert_finance import kobert_keyword

chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

today = datetime.datetime.now()
ymd = today.strftime("%Y-%m-%d")
month = today.strftime("%m")
day = today.strftime("%d")

#매일경제, 이데일리, 아시아경제, 한국경제, 머니투데이

news_dict = {
    "이데일리" : "1018",
    "아시아경제" : "1277",
    "매일경제" : "1009",
    "한국경제" : "1015",
    "머니투데이" : "1008"
}

def fun(news):
    
    url = driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.{month}.{day}&de=2025.{month}.{day}&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked={news_dict[news]}&nso=so%3Ar%2Cp%3Afrom20250201to20250301&is_sug_officeid=0&office_category=0&service_area=0")
    
    conn = pymysql.connect(
    host="158.247.211.92",
    user="milk",
    password="0621",
    database="kospi"
    )
    cursor = conn.cursor()
    
    news_data = []
    height = driver.execute_script("return document.body.scrollHeight")
    while True:
        boxs = driver.find_elements(By.XPATH, '//*[@data-block-id="news/prs_template_v2_news_tab_desk.ts"]/div/div/div/div')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break
        height = new_height
        print("스크롤 끝남")
        
    if news == "이데일리":
        for i, box in enumerate(boxs):
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            
            #print(box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href"))
            print(link)
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(3)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)
            
            title = driver.title

            try:
                date = driver.find_element(By.CSS_SELECTOR, ".dates ul li p:first-child").text
                date = date.replace("등록", "")
                if "오후" in date:
                    period = "PM"
                    date = date.replace("오후", "")
                elif "오전" in date:
                    period = "AM"
                    date = date.replace("오전", "")
                date = date.strip()
                date = f"{date} {period}"
                print(date)
            except :
                print("이데일리 날짜 패스")
                pass
            
            news_body = driver.find_element(By.CLASS_NAME, "news_body")
            inner_html = news_body.get_attribute("innerHTML")

            #bs를 이용해 html파싱
            soup = BeautifulSoup(inner_html, "html.parser")
            
            #태그에서 직계자손만 검색
            for child in soup.find_all(recursive=False):
                #직계자손 html에서 삭제
                child.decompose()
            
            content = soup.get_text(strip=True)
            # con_text = " ".join([p.strip().replace("\n", " ") for p in content])
            
            try:
                img = news_body.find_element(By.TAG_NAME, "img").get_attribute("src")
                time.sleep(2)
            except:
                img = ""
                
            time.sleep(2)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            date = date.replace(".", "-")
            secondExists = date.split(":")
            if len(secondExists) <= 2 :
                date += ":00"
            try:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S %p")
            except:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            dict = {
                "name" : news,
                "title" : title.strip(),
                "link" : link.strip(),
                "content" : content.strip(),
                "img" : img.strip(),
                "date" : dt
            }
            
            news_data.append(dict)
            print(dict)
            news_insert = """insert into news(name, title, link, content, img, date) select %s, %s, %s, %s, %s, %s from dual where not exists
            (
                select name, title from news where name = %s and title = %s
            )"""
            cursor.execute(news_insert, (news, dict["title"], dict["link"], dict["content"], dict["img"], dt, news, dict["title"]))

            conn.commit()

            if cursor.lastrowid > 0:
                #cursor.lastrowid = 114 or 115 일반 숫자
                #keyword = [1,2,3] 리스트
                senti_result, keywords, percentages = kobert_keyword(content)

                print(cursor.lastrowid)

                last_row_id = [cursor.lastrowid] * len(keywords)
                print(last_row_id)
                print(keywords) 
                data = list(zip(last_row_id, keywords))
                
                #뉴스가 인서트됨
                #키워드 테이블에 인서트
                keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
                cursor.executemany(keyword_insert,(data))
                conn.commit()

                bad, mid, good = percentages
                senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
                cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
                conn.commit()
            
    elif news == "아시아경제":
        for i, box in enumerate(boxs):
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            
            #print(box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href"))
            print(link)
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(3)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)
            
            title = driver.title

            try:
                date = driver.find_element(By.CSS_SELECTOR, ".date_box p").text
                date = date.replace("입력", "")
                print(date)
            except:
                print("아시아경제 날짜 패스")
                pass
            
            div = driver.find_element(By.CLASS_NAME, "article")
            content = div.find_elements(By.CSS_SELECTOR, "p")
            con_text = " ".join([p.text.strip().replace("\n", " ") for p in content])

            try:
                img = div.find_element(By.TAG_NAME, "img").get_attribute("src")
                time.sleep(2)
            except:
                img = ""
                
            time.sleep(2)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            date = date.replace(".", "-")
            secondExists = date.split(":")
            if len(secondExists) <= 2 :
                date += ":00"
            try:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S %p")
            except:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            dict = {
                "name" : news,
                "title" : title.strip(),
                "link" : link.strip(),
                "content" : con_text.strip(),
                "img" : img.strip(),
                "date" : dt
            }
            
            news_data.append(dict)
            print(dict)
            news_insert = """insert into news(name, title, link, content, img, date) select %s, %s, %s, %s, %s, %s from dual where not exists
            (
                select name, title from news where name = %s and title = %s
            )"""
            cursor.execute(news_insert, (news, dict["title"], dict["link"], dict["content"], dict["img"], dt, news, dict["title"]))

            conn.commit()

            if cursor.lastrowid > 0:
                #cursor.lastrowid = 114 or 115 일반 숫자
                #keyword = [1,2,3] 리스트
                senti_result, keywords, percentages = kobert_keyword(con_text)

                print(cursor.lastrowid)

                last_row_id = [cursor.lastrowid] * len(keywords)
                print(last_row_id)
                print(keywords) 
                data = list(zip(last_row_id, keywords))
                
                #뉴스가 인서트됨
                #키워드 테이블에 인서트
                keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
                cursor.executemany(keyword_insert,(data))
                conn.commit()

                bad, mid, good = percentages
                senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
                cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
                conn.commit()
            
    elif news == "매일경제":
        for i, box in enumerate(boxs):
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(1)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)
            
            title = driver.title

            try:
                date = driver.find_element(By.CSS_SELECTOR, ".time_area dl dd").text
            except:
                print("매일경제 날짜 패스")

            thumb = driver.find_element(By.CSS_SELECTOR, "#container > section.contents > div.news_detail_body_group > section > div.min_inner > div.sec_body > div.news_cnt_detail_wrap > div.thumb_area.img > figure > div")
            try:
                img = thumb.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                img = ""
            div = driver.find_element(By.CLASS_NAME, "news_cnt_detail_wrap")
            content = div.find_elements(By.CSS_SELECTOR, "p")
            con_text = " ".join([p.text.strip().replace("\n", " ") for p in content])
            time.sleep(2)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            date = date.replace(".", "-")
            secondExists = date.split(":")
            if len(secondExists) <= 2 :
                date += ":00"
            try:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S %p")
            except:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            dict = {
                "name" : news,
                "title" : title.strip(),
                "link" : link.strip(),
                "content" : content.strip(),
                "img" : img.strip(),
                "date" : dt
            }
            
            news_data.append(dict)
            print(dict)
            news_insert = """insert into news(name, title, link, content, img, date) select %s, %s, %s, %s, %s, %s from dual where not exists
            (
                select name, title from news where name = %s and title = %s
            )"""
            cursor.execute(news_insert, (news, dict["title"], dict["link"], dict["content"], dict["img"], dt, news, dict["title"]))

            conn.commit()

            if cursor.lastrowid > 0:
                #cursor.lastrowid = 114 or 115 일반 숫자
                #keyword = [1,2,3] 리스트
                senti_result, keywords, percentages = kobert_keyword(con_text)

                print(cursor.lastrowid)

                last_row_id = [cursor.lastrowid] * len(keywords)
                print(last_row_id)
                print(keywords) 
                data = list(zip(last_row_id, keywords))
                
                #뉴스가 인서트됨
                #키워드 테이블에 인서트
                keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
                cursor.executemany(keyword_insert,(data))
                conn.commit()

                bad, mid, good = percentages
                senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
                cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
                conn.commit()

    elif news == "한국경제":
        for i, box in enumerate(boxs):
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(3)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)
            
            title = driver.title

            try:
                date = driver.find_element(By.CSS_SELECTOR, ".txt-date").text
            except:
                print("한국경제 날짜 패스")

            news_body = driver.find_element(By.CLASS_NAME, "article-body")
            inner_html = news_body.get_attribute("innerHTML")
            #bs를 이용해 html파싱
            soup = BeautifulSoup(inner_html, "html.parser")
            
            #태그에서 직계자손만 검색
            for child in soup.find_all(recursive=False):
                #직계자손 html에서 삭제
                child.decompose()
            
            content = soup.get_text(strip=True)
            # con_text = " ".join([p.text.strip().replace("\n", " ") for p in content])
            try:
                img = news_body.find_element(By.TAG_NAME, "img").get_attribute("src")
                time.sleep(2)
            except:
                img = ""
                
            time.sleep(2)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            date = date.replace(".", "-")
            secondExists = date.split(":")
            if len(secondExists) <= 2 :
                date += ":00"
            try:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S %p")
            except:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            dict = {
                "name" : news,
                "title" : title.strip(),
                "link" : link.strip(),
                "content" : content.strip(),
                "img" : img.strip(),
                "date" : dt
            }
            
            news_data.append(dict)
            print(dict)
            news_insert = """insert into news(name, title, link, content, img, date) select %s, %s, %s, %s, %s, %s from dual where not exists
            (
                select name, title from news where name = %s and title = %s
            )"""
            cursor.execute(news_insert, (news, dict["title"], dict["link"], dict["content"], dict["img"], dt, news, dict["title"]))

            conn.commit()

            if cursor.lastrowid > 0:
                #cursor.lastrowid = 114 or 115 일반 숫자
                #keyword = [1,2,3] 리스트
                senti_result, keywords, percentages = kobert_keyword(content)

                print(cursor.lastrowid)

                last_row_id = [cursor.lastrowid] * len(keywords)
                print(last_row_id)
                print(keywords) 
                data = list(zip(last_row_id, keywords))
                
                #뉴스가 인서트됨
                #키워드 테이블에 인서트
                keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
                cursor.executemany(keyword_insert,(data))
                conn.commit()

                bad, mid, good = percentages
                senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
                cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
                conn.commit()
            
            
            
    elif news == "머니투데이":
        for i, box in enumerate(boxs):
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(3)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)
            
            title = driver.title

            try:
                date = driver.find_element(By.CSS_SELECTOR, ".date>time").text
            except:
                print("머니투데이")
                pass
            

            news_body = driver.find_element(By.ID, "textBody")
            inner_html = news_body.get_attribute("innerHTML")
            #bs를 이용해 html파싱
            soup = BeautifulSoup(inner_html, "html.parser")
            
            #태그에서 직계자손만 검색
            for child in soup.find_all(recursive=False):
                #직계자손 html에서 삭제
                child.decompose()
            
            content = soup.get_text(strip=True)
            # con_text = " ".join([p.text.strip().replace("\n", " ") for p in content])
            
            try:
                img = news_body.find_element(By.TAG_NAME, "img").get_attribute("src")
                time.sleep(2)
            except:
                img = ""
                
            time.sleep(2)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            date = date.replace(".", "-")
            secondExists = date.split(":")
            if len(secondExists) <= 2 :
                date += ":00"
            try:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M:%S %p")
            except:
                dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            dict = {
                "name" : news,
                "title" : title.strip(),
                "link" : link.strip(),
                "content" : content.strip(),
                "img" : img.strip(),
                "date" : dt
            }
            
            news_data.append(dict)
            print(dict)
            news_insert = """insert into news(name, title, link, content, img, date) select %s, %s, %s, %s, %s, %s from dual where not exists
            (
                select name, title from news where name = %s and title = %s
            )"""
            cursor.execute(news_insert, (news, dict["title"], dict["link"], dict["content"], dict["img"], dt, news, dict["title"]))

            conn.commit()

            if cursor.lastrowid > 0:
                #cursor.lastrowid = 114 or 115 일반 숫자
                #keyword = [1,2,3] 리스트
                senti_result, keywords, percentages = kobert_keyword(content)

                print(cursor.lastrowid)

                last_row_id = [cursor.lastrowid] * len(keywords)
                print(last_row_id)
                print(keywords) 
                data = list(zip(last_row_id, keywords))
                
                #뉴스가 인서트됨
                #키워드 테이블에 인서트
                keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
                cursor.executemany(keyword_insert,(data))
                conn.commit()

                bad, mid, good = percentages
                senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
                cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
                conn.commit()
  
            else:
                #뉴스가 중복되어서 인서트 안함
                #단어 인서트 안해도됨
                pass

    print(f"{news} 저장!")

    cursor.close()
    conn.close()


# fun("매일경제")

#매일경제, 이데일리, 아시아경제, 한국경제, 머니투데이
#스케줄러
schedule.every(1).minutes.at(":00").do(fun, "이데일리")
schedule.every(1).minutes.at(":03").do(fun, "아시아경제")
schedule.every(1).minutes.at(":09").do(fun, "매일경제")
schedule.every(1).minutes.at(":06").do(fun, "한국경제")
schedule.every(1).minutes.at(":12").do(fun, "머니투데이")
while True:
    schedule.run_pending()
    time.sleep(2)
