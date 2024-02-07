import pandas as pd 
import json

# Load the CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\tebne\OneDrive\Programming\Python\Written\Data\EURCAD26.csv', sep='\t')

# Get the '<CLOSE>' EURUSD_data
data = df['<CLOSE>'].values.tolist()
with open(r'Test_\Data.py', 'a') as file:
   json.dump(data, file)