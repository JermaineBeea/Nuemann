from forex_python.converter import CurrencyRates

import dateutil.parser as dateutil

def forex(mode, basecurr, countercurr_date = None, date_amount = None, date = None):
   mode_keys = 'get rates', 'get rate', 'convert'
   modelist = CurrencyRates().get_rates, CurrencyRates().get_rate, CurrencyRates().convert
   arguments = [basecurr, countercurr_date, date_amount, date]

   if mode not in mode_keys:
      return f'Error: Enter one of {mode_keys}'
   try:
      key_index = mode_keys.index(mode)
      if arguments[key_index + 1] is not None:
         arguments[key_index + 1] = dateutil.parse(arguments[key_index + 1])
      modecalled = modelist[key_index](*arguments[:key_index + 2])
      return modecalled
   except Exception as e:
      return f'Error: {e}'


