import json

# Slippages time window in seconds
TIME_WINDOW = 5

# Max time
MAX_TIME = 0

# Load bitstamp data
data = {}

# Store slippages to use for statistics calculation
slippages = { 'bids': [], 'asks': [], 'bids_percentage': [], 'asks_percentage': [] }

# Dynamic programming to save average prices for determined timestamps
dp = {}

def read_data():
  global data, MAX_TIME

  f = open('historical_prices_bitstamp_4h.json', 'r')
  file_data = json.loads(f.read())
  data = file_data['data']
  MAX_TIME = file_data['max_time']

  f.close()

def find_entry(time, index):
  global data

  if time in dp: return dp[time]

  time_start = float(data[0]['timestamp'])

  if not time: return (data[0], index)

  while index < len(data):
    if int(data[index]['microtimestamp'])/10**6 - time_start > time:
      dp[time] = (data[index-1], index)
      return dp[time]
    
    index += 1

def calculate_slippages():
  global slippages

  time = 0

  first_index = 0
  second_index = 0

  while time < MAX_TIME - TIME_WINDOW:
    (first_entry, first_index) = find_entry(time, first_index)
    (second_entry, second_index) = find_entry(time + TIME_WINDOW, second_index)

    time += 1
    # time += TIME_WINDOW

    bids_slippage = first_entry['average_bids_price'] - second_entry['average_bids_price']
    asks_slippage = first_entry['average_asks_price'] - second_entry['average_asks_price']
    slippages['bids'].append(bids_slippage)
    slippages['bids_percentage'].append(bids_slippage/first_entry['average_bids_price'])
    slippages['asks'].append(asks_slippage)
    slippages['asks_percentage'].append(asks_slippage/first_entry['average_asks_price'])

  slippages['sample_size'] = len(slippages['bids'])
  
  f = open('slippages_4h.json', 'w')
  f.write(str(json.dumps(slippages)))

  f.close()

if __name__ == '__main__':
  read_data()
  calculate_slippages()
  