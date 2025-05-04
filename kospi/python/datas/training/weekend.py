from holidayskr import is_holiday
from datetime import date, datetime

def is_weekend(date):
    return date.weekday() < 5

today = date.today()
print(today)

day = date(2025, 5, 6)

# 0~4-평일, 5,6-주말
if is_weekend(day):
    #평일
    if is_holiday(str(day)):
        print("평일, 공휴일")
    else:
        print("그냥 평일")
else:
    #주말
    print("주말")
