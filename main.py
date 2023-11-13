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

# Parameters for calling the alpha vantage API.
alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY
}

# Get the stock data from the api.
stock_data = requests.get(url=ALPHA_ENDPOINT, params=alpha_params)
stock_data.raise_for_status()

# Get the daily stock data.
daily_stock_data = stock_data.json()["Time Series (Daily)"]

# Get the stock data for yesterday and the day before.
yesterdays_date = list(daily_stock_data.keys())[0]
day_before_yesterday = list(daily_stock_data.keys())[1]

# Get the closing prices from yesterday and the day before.
yesterday_close = float(daily_stock_data[yesterdays_date]["4. close"])
dby_close = float(daily_stock_data[day_before_yesterday]["4. close"])

# Get the percentage difference.
percent_change = (yesterday_close - dby_close) / dby_close * 100

# Get today's date to get the most recent articles.
todays_date = str(datetime.date.today())

# The parameters for News API.
# Getting the 3 most recent articles in English.
news_api_params = {
    "apiKey": NEWS_API_KEY,
    "q": f"+\"{COMPANY_NAME}\"",
    "searchIn": "title",
    "to": todays_date,
    "language": "en",
    "pageSize": 3
}

# If the percentage change in closing prices is significant, send an email.
if percent_change >= SHIFT_AMOUNT or percent_change <= -SHIFT_AMOUNT:
    # Get the news stories.
    company_news = requests.get(url=NEWS_API_ENDPOINT, params=news_api_params)
    top_articles = company_news.json()["articles"]

    if percent_change > 0:
        change_symbol = "+"
    else:
        change_symbol = "-"

    # Write the message to be sent in email: The percentage change and the 3 most recent news stories.
    message = f"Subject:{STOCK} {change_symbol}{round(abs(percent_change))}%\n\n"
    for article in top_articles:
        message += f"""
Headline: {article['title']}
By {article['author']} from {article['source']['name']}
Brief: {article['description']}
Source: {article['url']}\n\n
                    """

    # Replace unicode characters so the message is properly sent through email.
    message = message.replace("…", "...")
    message = message.replace("–", "-")

    sender = "dwdeathwolf@gmail.com"
    receiver = "jhecker2001@gmail.com"
    g_pass = "nezinvlcxjckceys"

    # Send the email.
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=sender, password=g_pass)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg=f"{message}"
        )

