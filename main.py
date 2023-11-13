import requests
# import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = "QRC21Y77Q40OYV1W"

alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY
}

# # STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_data = requests.get(url="https://www.alphavantage.co/query", params=alpha_params)
stock_data.raise_for_status()

stock_json = stock_data.json()["Time Series (Daily)"]

yesterdays_date = list(stock_json.keys())[0]
day_before_yesterday = list(stock_json.keys())[1]

yesterday_close = float(stock_json[yesterdays_date]["4. close"])
dby_close = float(stock_json[day_before_yesterday]["4. close"])

percent_change = (yesterday_close - dby_close) / dby_close * 100

print(f"Percent change is {percent_change}%.")
if percent_change >= 5 or percent_change <= -5:
    print("Get News")
else:
    print("None")

# # STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# # STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and
# prominent investors are required to file by the SEC The 13F filings show the funds' and
# investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and
# prominent investors are required to file by the SEC The 13F filings show the funds' and
# investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

