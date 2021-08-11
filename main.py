import requests
import json
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY_ALPHA = ""
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"

API_KEY_NEWS = ""
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""

parameters_alpha = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_ALPHA,
}



get_news = False
response = requests.get(ALPHA_ENDPOINT, params=parameters_alpha)
daily_stock_price = response.json()["Time Series (Daily)"]
daily_stock_price_list = [value for (key, value) in daily_stock_price.items()]
yesterday_closing_status = float(daily_stock_price_list[0]["4. close"])
day_before_yesterday_closing_status = float(daily_stock_price_list[1]["4. close"])


percentage_change = (yesterday_closing_status - day_before_yesterday_closing_status) / yesterday_closing_status * 100
if percentage_change < -3 or percentage_change > 3:
    get_news = True

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

if get_news:
    parameters_news = {
        "q": COMPANY_NAME,
        "apikey": API_KEY_NEWS,
        "pagesize": "3"
    }
    response = requests.get(NEWS_ENDPOINT, params=parameters_news)
    first_three_articles = [news for news in response.json()["articles"]]
    # with open("t.txt", "w") as file:
    #     a = response.json()["articles"][0]
    #     file.write(json.dumps(first_three_articles[0]))


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def generate_messege(stock, percentage, headline, brief ):
    if percentage > 0:
        symbol = "🔺"
    else:
        symbol = "🔻"
    message_template = f"{stock}: {symbol}{round(percentage)}%\n\nHeadline: {headline}\n\nBrief: {brief}"
    return message_template


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
for news in first_three_articles:
    to_send = generate_messege(STOCK, percentage_change, news["title"], news["description"])
    message = client.messages \
        .create(
        body=to_send,
        from_="+14133411508",
        to='+917857942538'
    )
    print(message.status)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

