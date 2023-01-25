import json
import pandas as pd


df_list = []
df_list.append(pd.read_csv('funds.csv'))
df = pd.read_csv('funds_data.csv')
df_list.append(df)

json_cols = ['cashDividends', 'subscriptions', 'stockDividends']

for col in json_cols:
    df[col] = df[col].str.replace("'", '"')
    df[col] = df[col].apply(json.loads)
    data = [
    pd.DataFrame.from_records(getattr(row, col)) \
                .assign(code=getattr(row, 'code')) 
                for row in df.itertuples()
                if len(getattr(row, col)) > 0 ]
    if len(data) == 0:
        continue
    df2 = pd.concat(data)
    df_list.append(df2)
    #df2.to_csv(f'funds_data_{col}.csv', index=False)

NUM_COLS = ['detailFund.quotaCount', 'tradingLot', 'quantity', 'rate', 'percentage', 'priceUnit', 'factor']
DT_COLS = ['quotedPer', 'detailFund.quotaDateApproved', 'paymentDate', 'approvedOn', 'lastDatePrior', 'subscriptionDate']
FILES = ['base', 'detail' ,'cash_divs', 'subscriptions', 'stock_divs']

for i, df in enumerate(df_list):
    
    for c in NUM_COLS:
        if c not in df.columns or df[c].dtype != 'object':
            continue
        
        df[c] = df[c].str.replace('.', '', regex=False).replace(',', '.')
        df[c] = pd.to_numeric(df[c], errors='coerce')
    
    for c in DT_COLS:
        if c not in df.columns:
            continue

        df[c] = pd.to_datetime(df[c], errors='coerce', dayfirst=True)
    
    df.drop(columns=['Unnamed: 0'], errors='ignore').to_csv(f'fidata/fi_{FILES[i]}.csv', index=False)