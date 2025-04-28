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

    label_list = df["date"].values.tolist()
    print(df["date"])
    open_list = df["Open"].tolist()
    print(df["Open"])
    high_list = df["High"].tolist()
    low_list = df["Low"].tolist()
    close_list = df["Close"].tolist()

    data = {
    "labels": label_list,
    "open": open_list,
    "high": high_list,
    "low": low_list,
    "close": close_list
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
