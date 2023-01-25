import time
import requests
from python_retry import retry
import pandas as pd

def run(urls, url_pat, filename, interval=0.4):
    urls = set([l.strip() for l in lines 
                        if url_pat in l])
    df = pd.DataFrame()
    for url in urls:
        data = get_data(url)
        df = pd.concat([df, data])
        time.sleep(interval)

    df.to_csv(filename, index=False)


@retry()
def get_data(url):
    r = requests.get(url)
    r.raise_for_status()
    data = pd.json_normalize(r.json())
    data['url'] = url
    return data


with open('raw/fii_urls.txt', 'r') as f:
    lines = f.readlines()


source = [('GetDetailFundSIG', 'funds.csv'), 
           ('GetListedSupplementFunds', 'funds_data.csv')]
for pat, name in source:
    run(lines, pat, name)