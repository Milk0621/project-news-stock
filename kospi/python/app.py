from flask import Flask, jsonify, render_template, request
import yfinance as yf
from flask_cors import CORS
from zoneinfo import ZoneInfo
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/stock/<symbol>")
def stock_data(symbol):
    symbol = "^KS11"
    df = yf.download(symbol, period="5d", interval="1m")
    df["date"] = df.index.tz_convert(ZoneInfo("Asia/Seoul"))
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M")
    
    arr_2d = np.array(df["Close"].values.tolist())
    label_list = df["date"].values.tolist()
    close_list = arr_2d.reshape(-1).tolist()
    
    dict_list = []
    for i in range(len(label_list)):
        dict_list.append({"lebels" : label_list[i], "close" : close_list[i]})
    data = {
        "labels" : label_list,
        "close" : close_list
    }
    print(dict_list)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
