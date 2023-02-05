from twilio.rest import Client
from datetime import datetime, timedelta
import yfinance as yf

def scraper(symbol):

    tickerSymbol = symbol
    tickerData = yf.Ticker(tickerSymbol)

    startDate = datetime.today().strftime('%Y-%m-%d')
    endDate = datetime.today() + timedelta(1)
    endDate = endDate.strftime('%Y-%m-%d')

    tickerDf = tickerData.history(period='1d', start=startDate, end=endDate, interval='1h')

    return tickerDf

def Analyser(stockData, dataPoints, stock):

    for point in dataPoints:

        value, trigger = point
        if trigger.lower() == 'above' and stockData['Close'][-1] >= value:
            message = f"Stock: {stock} reached the trigger, Stock Price Above: {value}"
            sendMessage(str(message))
        elif trigger.lower() == 'below' and stockData['Close'][-1] <= value:
            message = f"Stock: {stock} reached the trigger, Stock Price Below: {value}"
            sendMessage(str(message))

def sendMessage(message):

    accountSID = 'ACe91fcece23f80f79896add25d4d79250'
    AuthToken = '1a4928328969389bc5b12d679ba14850'
    phoneNo = '+12136933279'

    client = Client(accountSID, AuthToken)

    message = client.messages.create(
                        body=message,
                        from_=phoneNo,
                        to='+918688425005'
                    )

    print(message.sid)

def looping(list):
    for stock in list:
        print(stock)
        stockData = scraper(stock)
        Analyser(stockData, list[stock], stock)


list = {
        'PNB.NS': [[45.00, 'Below'], [57.00, 'Above']],
        'ZOMATO.NS': [[62.00, 'Below'], [70.00, 'Above']]
        }

looping(list)