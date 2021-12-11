import pandas as pd
from googleapiclient import discovery
sheet_id = '1IOJSsKBvvNKOfL_WckYK9iuC7G4CqHtUz_F6dbd6BN8'
url = 'export?format=csv'

data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/{url}")
dataDict = data.to_dict(orient='dataDict')


print(dataDict)