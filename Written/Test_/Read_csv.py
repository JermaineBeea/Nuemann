import pandas as pd 
import json

def readcsv(filename, write = False, writename = None):
   df = pd.read_csv(filename, sep='\t')
   data = df['<CLOSE>'].values.tolist()
   if write:
      with open(writename, 'a') as file:
         json.dump(data, file)
   
   return data
