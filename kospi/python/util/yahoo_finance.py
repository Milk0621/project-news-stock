import yfinance as yf
import pandas as pd
import mplfinance as mpf

ticker = "^KS11"
cospi = yf.download(ticker, start="2023-01-01", end="2024-01-01", multi_level_index=False)
#cospi.columns = cospi.columns.get_level_values(0)

#print(cospi.info())

#print(type(cospi.index))

#print(cospi.columns)

#index
#cospi.index = pd.to_datetime(cospi.index)

# cospi["date"] = cospi.index

#cospi = cospi.reset_index()

print(cospi)

# mpf.plot(cospi, type="candle", style="charles", savefig="chart.png")