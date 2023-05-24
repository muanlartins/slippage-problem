import json

# Slippages time window in seconds
TIME_WINDOW = 5

# Max time
MAX_TIME = 0

data = {}
slippages = { 'bids': [], 'asks': []}

def read_data():
  global data, MAX_TIME

  f = open('historical_prices_bitstamp.json', 'r')
  file_data = json.loads(f.read())
  data = file_data['data']
  MAX_TIME = file_data['max_time']

  f.close()

def find_entry(time):
  global data

  time_start = float(data[0]['timestamp'])

  if not time: return data[0]

  for i in range(len(data)):
    if int(data[i]['microtimestamp'])/10**6 - time_start > time:
      return data[i-1]

def calculate_slippages():
  global slippages

  time = 0

  while time < MAX_TIME - TIME_WINDOW:
    first_entry = find_entry(time)
    second_entry = find_entry(time + TIME_WINDOW)

    time += 1

    bids_slippage = first_entry['average_bids_price'] - second_entry['average_bids_price']
    asks_slippage = first_entry['average_asks_price'] - second_entry['average_asks_price']
    slippages['bids'].append(bids_slippage)
    slippages['asks'].append(asks_slippage)

  
  f = open('slippages.json', 'w')
  f.write(str(json.dumps(slippages)))

  f.close()

if __name__ == '__main__':
  read_data()
  calculate_slippages()
  