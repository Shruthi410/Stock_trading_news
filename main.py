import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api = "E2JIJCWRK094OUAD"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api
}

news_api = "b1f50f9780314af5916ab4b29658d528"
news_parameters = {
    "apikey": news_api,
    "qInTitle": COMPANY_NAME
}

twilio_acc_sid = "ACb2d1c08812aaae3c9f6ec9466b66757b"
twilio_auth_token = "5298df444e3ad4be7f0c5b7080a6b47d"
twilio_phone = "+16094388802"
twilio_registered_phone = "+91<YOUR REGISTERED MOBILE NUMBER>"


stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data = stock_response.json()
print(data)

close_yestersay = data["Time Series (Daily)"]["2021-04-14"]["4. close"]
close_day_before = data["Time Series (Daily)"]["2021-04-13"]["4. close"]

difference = float(close_day_before) - float(close_yestersay)
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
difference_percent = round((difference / float(close_yestersay)) * 100)

print(difference)
print(difference_percent)

if difference_percent >= 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)
    formatted_articles = [f"{STOCK}: {up_down}{difference_percent}%\nHeadline: {article['title']}\n Brief: {article['description']}" for article in three_articles]
    account_sid = twilio_acc_sid
    auth_token = twilio_auth_token
    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_=twilio_phone,
            to=twilio_registered_phone
        )

#you can format your message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

