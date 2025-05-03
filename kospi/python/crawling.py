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

driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.02.01&de=2025.02.01&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked=1018&nso=so%3Ar%2Cp%3Afrom20250201to20250415&is_sug_officeid=0&office_category=0&service_area=0")

dates = datetime.datetime(2025, 4, 21)
# end = datetime.datetime(2025, 1, 31)
# dates = dates + datetime.timedelta(days=11) 

print(dates) #4월 17일

#언론사, 타이틀, 링크, 날짜, 본문, 이미지
#이데일리, 아시아경제, 매일경제, 한국경제, 머니투데이
#1018, 1277, 1009, 1015, 1008
news_id = ["1009", "1015", "1008"]

news_data=[]
for i in range(0, 11):
    month = dates.strftime("%m")
    day = dates.strftime("%d")
    for id in news_id:

        driver.get(f"https://search.naver.com/search.naver?where=news&query=%EC%BD%94%EC%8A%A4%ED%94%BC&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2025.{month}.{day}&de=2025.{month}.{day}&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked={id}&nso=so%3Ar%2Cp%3Afrom20250201to20250415&is_sug_officeid=0&office_category=0&service_area=0")

        time.sleep(2)
        boxs = None
        height = driver.execute_script("return document.body.scrollHeight")
        try:
            while True:
                #Ermefm6A3ilpd9Zvt0OZ
                boxs = driver.find_elements(By.XPATH, '//*[@data-block-id="news/prs_template_v2_news_tab_desk.ts"]/div/div/div/div')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if height == new_height:
                    break
                height = new_height
        except:
            continue
        
        for i, box in enumerate(boxs):
            con_text= None
            time.sleep(2)
            #bynlPWBHumGsbotLYK9A jT1DuARpwIlNAFMacxlu
            link = box.find_elements(By.XPATH, "./div")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            time.sleep(2)
            driver.execute_script(f"window.open('{link}', '_blank')")
            time.sleep(1)

            #새 탭으로 전환
            driver.switch_to.window(driver.window_handles[1])
            #현재 열려있는 탭중 2번째 탭으로(1번 인덱스)로 전환
            time.sleep(2)

            #제목
            title = driver.title
            try:

                #날짜(시간)
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

                try:
                    date = driver.find_element(By.CSS_SELECTOR, ".txt-date").text
                except:
                    print("한국경제 날짜 패스")

                try:
                    date = driver.find_element(By.CSS_SELECTOR, ".date>time").text
                except:
                    print("머니투데이")
                    pass

                #본문
                #이데일리 : news_body, 한국경제 : article-body, 머니투데이 : textBody
                content = driver.find_element(By.XPATH, "//*[@class='news_body' or @class='article-body' or @id='textBody']")
                inner_html = content.get_attribute("innerHTML")
                time.sleep(2)

                soup = BeautifulSoup(inner_html, "html.parser")

                for child in soup.find_all(recursive=False):
                    #직계자손 html에서 삭제
                    child.decompose()
                
                con_text = soup.get_text(strip=True)
                
            except:
                print("bs 본문 못 찾음")
                pass
            
            try:
                if con_text:
                    print("던져!")
                    raise

                #날짜(시간)
                try:
                    date = driver.find_element(By.CSS_SELECTOR, ".date_box p").text
                    date = date.replace("입력", "")
                    print(date)
                except:
                    print("아시아경제 날짜 패스")
                    pass

                try:
                    date = driver.find_element(By.CSS_SELECTOR, ".time_area dl dd").text
                except:
                    print("매일경제 날짜 패스")

                #본문
                #아시아경제 : article, article_view , 매일경제 : news_cnt_detail_wrap
                content_box = driver.find_element(By.XPATH, "//*[@class='article_view' or @class='article' or @class='news_cnt_detail_wrap']")
                content = content_box.find_elements(By.CSS_SELECTOR, "p")

                con_text = " ".join([p.text.strip().replace("\n", " ") for p in content])
                print(dates, id, con_text)

            except:
                print("p 본문 못 찾음")
                pass

            try: 
                #이미지
                #이데일리 : news_body, 아시아경제 : img_link, 매일경제 : thumb, 한국경제 : figure-img, 머니투데이 : img
                img_box = driver.find_element(By.XPATH, "//*[@class='news_body' or @class='img_link' or @class='thumb' or @class='figure-img' or @class='img']")
                img = img_box.find_element(By.TAG_NAME, "img").get_attribute("src")
                #이데일리
            except:
                print("이미지 못 찾음")
                img = ""

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

            name = box.find_element(By.CSS_SELECTOR, ".sds-comps-text-type-body2").text
            dict = {
                "name" : name,
                "title" : title,
                "link" : link,
                "content" : con_text,
                "img" : img,
                "date" : dt
            }
            news_data.append(dict)
            print(f"{id}의 {i}번째 저장!")
            
    dates = dates + datetime.timedelta(days=1)

df = pd.DataFrame(news_data)
df.to_csv("./news_data2.csv", index=False)

driver.quit()