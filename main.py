import requests
import smtplib


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "LUQRV0EWPLGHCOV6"
NEWS_API_KEY = "6c0ed3db23a441fab08c2ab4f86b95be"

MY_EMAIL = "xyz@gmail.com" # use your email id
PASSWORD = "abc12345" # generate a password from email for this by which a third party can access your account

#  [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)


# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yes_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yes_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
difference = float(yesterday_closing_price) - float(day_before_yes_closing_price)
print(difference)
up_down = None
if difference > 0:
    up_down = "The prices are Up!!!"
else:
    up_down = "The prices are Down!!!"



# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference/float(yesterday_closing_price))*100)
print(diff_percent)


# If  percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 2:
    # Instead of printing ("Get News"), use the News API to get the first 3 articles related to the COMPANY_NAME.

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    # Create a new list of the first 3 article's headline and description using list comprehension.

    # formatted_articles = [f"{STOCK_NAME}: {up_down} by {diff_percent}% Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    for article in three_articles:
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        message = f"Subject: {STOCK_NAME}:{up_down} {article['title']}\n\n" \
                  f"{article['description']}".encode("utf-8")
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=message
        )
        connection.close()







