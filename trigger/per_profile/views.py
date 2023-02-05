from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
import yfinance as yf

def index(request):
    return render(request, 'per_profile/index.html')

def getstock(request):
    if request.method == 'POST' and 'stock' in request.POST:

        symbol = request.POST['stock']
        tickerSymbol = symbol
        tickerData = yf.Ticker(tickerSymbol)

        startDate = datetime.today().strftime('%Y-%m-%d')
        endDate = datetime.today() + timedelta(1)
        endDate = endDate.strftime('%Y-%m-%d')

        tickerDf = tickerData.history(period='1d', start=startDate, end=endDate, interval='2m')

        # Rounding of the data 
        tickerDf = tickerDf.round(3)

        if 'stock' in request.POST and ('abovetrigger' in request.POST or 'belowtrigger' in request.POST):
            price = request.POST['price-point']
            if 'abovetrigger' in request.POST:
                retval = setStockTrigger(symbol, price, 'above')
                if retval:
                    message = 'Above Trigger point created'
            else:
                retval = setStockTrigger(symbol, price, 'below')
                if retval:
                    message = 'below Trigger point created'

            context = {
             'df': tickerDf,
             'symbol': symbol,
             'message': message,
            }   

            return render(request, 'per_profile/index.html', context)
        
        elif 'stock' in request.POST:
            context = {
             'df': tickerDf,
             'symbol': symbol
            }

            return render(request, 'per_profile/index.html', context)
        else:
            return HttpResponse('wrong data form!!!')
    else:
        return HttpResponse('it didnt work!!!')
        

def setStockTrigger(stock, price, trigger):
    if stock.lower() in triggerList:
        triggerList[stock.lower()].append([price, trigger.lower()])
        print("TriggerList: ", triggerList)
        return True
    else:
        triggerList[stock.lower()] = [[price, trigger.lower()]]
        print("TriggerList: ", triggerList)
        return True

    
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

# def looping(list):
#     for stock in list:
#         print(stock)
#         stockData = scraper(stock)
#         Analyser(stockData, list[stock], stock)

triggerList = {}

# looping(list)




# Therse are the Vs code basics i am trying to master 
# trying to use the mouse as less as possible so that i can same time 
# need some extra lines of code 
# repeating the word time so that i can replace tiume multiple times