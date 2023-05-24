from math import sqrt
import json

mean = 0
variance = 0
standard_deviation = 0
bids_slippages = []
asks_slippages = []
data = {}

def read_data():
  global bids_slippages, asks_slippages

  f = open('slippages.json', 'r')

  slippages = json.loads(f.read())

  bids_slippages = slippages['bids']
  asks_slippages = slippages['asks']

  f.close()

def write_data():
  f = open('measures.json', 'w')

  f.write(str(json.dumps(data)))

  f.close()

def calculate_measures(slippages, side):
  global data, mean, variance, standard_deviation

  mean = sum(slippages)/len(slippages)

  for slippage in slippages:
    variance += (slippage - mean)**2
  
  variance /= len(slippages)

  standard_deviation = sqrt(variance)

  data[side] = {
    'mean': mean,
    'variance': variance,
    'standard_deviation': standard_deviation
  }

if __name__ == '__main__':
  read_data()
  calculate_measures(bids_slippages, 'bids')
  calculate_measures(asks_slippages, 'asks')
  write_data()