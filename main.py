import requests
import datetime
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = "QRC21Y77Q40OYV1W"
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_KEY = "253da3f883e54107bd488fb78cd853cb"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
SHIFT_AMOUNT = 5

alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY
}

# # STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_data = requests.get(url=ALPHA_ENDPOINT, params=alpha_params)
stock_data.raise_for_status()

daily_stock_data = stock_data.json()["Time Series (Daily)"]

yesterdays_date = list(daily_stock_data.keys())[0]
day_before_yesterday = list(daily_stock_data.keys())[1]

yesterday_close = float(daily_stock_data[yesterdays_date]["4. close"])
dby_close = float(daily_stock_data[day_before_yesterday]["4. close"])

percent_change = (yesterday_close - dby_close) / dby_close * 100

todays_date = str(datetime.date.today())

news_api_params = {
    "apiKey": NEWS_API_KEY,
    "q": f"+\"{COMPANY_NAME}\"",
    "searchIn": "title",
    "to": todays_date,
    "language": "en",
    "pageSize": 3
}

if percent_change >= SHIFT_AMOUNT or percent_change <= -SHIFT_AMOUNT:
    company_news = requests.get(url=NEWS_API_ENDPOINT, params=news_api_params)
    top_articles = company_news.json()["articles"]

    if percent_change > 0:
        change_symbol = "+"
    else:
        change_symbol = "-"

    message = f"Subject:{STOCK} {change_symbol}{round(abs(percent_change))}%\n\n"
    for article in top_articles:
        message += f"""
Headline: {article['title']}
By {article['author']} from {article['source']['name']}
Brief: {article['description']}
Source: {article['url']}\n\n
                    """

    message = message.replace("…", "...")
    message = message.replace("–", "-")
    sender = "dwdeathwolf@gmail.com"
    receiver = "jhecker2001@gmail.com"
    g_pass = "nezinvlcxjckceys"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=sender, password=g_pass)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg=f"{message}"
        )

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

