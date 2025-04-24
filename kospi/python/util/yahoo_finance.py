import yfinance as yf
import pandas as pd
import mplfinance as mpf
from zoneinfo import ZoneInfo
import numpy as np


ticker = "^KS11"
cospi = yf.download(ticker,  period="5d", interval="1m")
cospi["date"] = cospi.index.tz_convert(ZoneInfo("Asia/Seoul"))
#cospi = cospi.reset_index()

cospi["date"] = cospi["date"].dt.strftime("%Y-%m-%d %H:%M")
print(cospi["date"].values.tolist())

arr_2d = np.array(cospi["Close"].values.tolist())

label_list = cospi["date"].values.tolist()
close_list = arr_2d.reshape(-1).tolist()
dict_list = []
for i in range(len(label_list)):
    dict_list.append({"lebels" : label_list[i], "close" : close_list[i]})

data = {
        "labels" : cospi["date"].values.tolist(),
        "close" : arr_2d.reshape(-1).tolist()
    }
print(dict_list)

