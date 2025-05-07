import pandas as pd

finance = pd.read_csv("./datas/dict/finance_data.csv")

finance = finance[["labels", "word"]]

finance["labels"] = finance["labels"].map({"positive":0, "neutral":1, "negative":2})

finance.to_csv("./datas/dict/finance.csv", index=False)