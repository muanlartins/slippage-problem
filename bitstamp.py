import websocket
import json
import ssl
import sys
from time import sleep
from datetime import datetime

# Desired amount of BTC
AMOUNT = 1

# Minutes collecting data from bitstamp
MINUTES = 180

bitstamp_endpoint = 'wss://ws.bitstamp.net'
data = []
prices = []
f = 0
first_microtimestamp = 0

def calculate_average_price(entry, side):
  offers = entry[side]

  average_price = 0
  current_amount = 0

  for offer in offers:
    offer_price = float(offer[0])
    offer_amount = float(offer[1])

    if current_amount + offer_amount >= AMOUNT:
      average_price += (AMOUNT - current_amount) * offer_price
      break
    else:
      average_price += offer_price * offer_amount
      current_amount += offer_amount
    
  return average_price

def subscribe_marketdata(ws):
  params = {
    'event': 'bts:subscribe',
    'data': {
        'channel': 'order_book_btcusd'
    }
  }
  market_depth_subscription = json.dumps(params)

  ws.send(market_depth_subscription)


def on_open(ws):
  print('web-socket connected.')
  subscribe_marketdata(ws)

def on_message(ws, response):
  global data, f, first_microtimestamp

  data = json.loads(response)['data']

  data['average_bids_price'] = calculate_average_price(data, 'bids')
  data['average_asks_price'] = calculate_average_price(data, 'asks')
  del data['bids']
  del data['asks']

  timestamp = int(data['timestamp'])
  microtimestamp = int(data['microtimestamp'])

  prices.append(data)

  if not first_microtimestamp: first_microtimestamp = microtimestamp

  time_elapsed = (microtimestamp - first_microtimestamp)/(10**6)

  print(time_elapsed)

  if time_elapsed > MINUTES*60:
    f = open('historical_prices_bitstamp.json', 'w')

    bitstamp_data = { 'data': prices, 'max_time': MINUTES*60 }
    bitstamp_json = json.dumps(bitstamp_data)
    f.write(str(bitstamp_json))

    f.close()

    sys.exit()

def on_error(ws, msg):
  print(msg)

if __name__ == '__main__':
  marketdata_ws = websocket.WebSocketApp(bitstamp_endpoint, on_open=on_open, on_message=on_message, on_error=on_error)
  marketdata_ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})