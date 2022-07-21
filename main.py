import requests as rq
from datetime import datetime, timedelta
from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'AC5173cb3cd52ad28d247eef71b6a3b229'
TWILIO_AUTH_TOKEN = '777a387d30987f61adeafaa4ebc7b7cc'
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = 'AE52FHVQARTOXTA8'
STOCK_API_PARAMETERS = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY
}

NEWS_API_KEY = 'aac88f9e454f40b085d5993adbf00b7b'
NEW_API_PARAMETERS = {
    'q': COMPANY_NAME,
    'apiKey': NEWS_API_KEY
}

# STEP 1: Use https://newsapi.org/docs/endpoints/everything
stock_response = rq.get(url=STOCK_ENDPOINT, params=STOCK_API_PARAMETERS)
stock_response.raise_for_status()
print(stock_response.json())
stock_data = stock_response.json()
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the
# two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
date_keys = list(stock_data['Time Series (Daily)'].keys())
yesterday_closing_price = float(stock_data["Time Series (Daily)"][date_keys[0]]["4. close"])
day_before_yesterday_closing_price = float(stock_data["Time Series (Daily)"][date_keys[1]]["4. close"])

# HINT 2: Work out the value of 5% of yesterday's closing stock price.
stock_price_diff = yesterday_closing_price - day_before_yesterday_closing_price
precentage_diff = abs(round(stock_price_diff / day_before_yesterday_closing_price * 100))
print(precentage_diff)
client = Client(account_sid, auth_token)
if precentage_diff >= 5 or precentage_diff <= -5:
    # STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    # HINT 1: Think about using the Python Slice Operator
    news_response = rq.get(url=NEWS_ENDPOINT, params=NEW_API_PARAMETERS)
    news_data = news_response.json()
    company_news = [news_data["articles"][i] for i in range(0, 3)]
    print(company_news)
    news = []
    for n in company_news:
        item = {
            'Headlines': n['title'],
            'Brief': n['description']
        }
        news.append(item)
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    # HINT 1: Consider using a List Comprehension.

    for news_article in news:
        if precentage_diff >= 5:
            message = client.messages \
                .create(
                body=f'{STOCK}: 🔺{precentage_diff} %\n\nHeadline:{news_article["Headlines"]}\n\n{news_article["Brief"]}',
                from_='+17125265712',
                to='+234 810 667 1579'
            )
            print(message.status)
        elif precentage_diff <= -5:
            message = client.messages \
                .create(
                body=f'{STOCK}: 🔻{precentage_diff} %\n\nHeadline:{news_article["Headlines"]}\n\n{news_article["Brief"]}',
                from_='+17125265712',
                to='+234 810 667 1579'
            )
            print(message.status)

else:
    message = client.messages \
        .create(
        body='Stock prices haven\'t made any significant movement',
        from_='+17125265712',
        to='+234 810 667 1579'
    )
    print(message.status)


