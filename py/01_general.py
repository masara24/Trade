
import efinance as ef
import pandas as pd
import datetime
import sys

h = "python general.py DELL 20250308"
if len(sys.argv)-1 !=2: sys.exit(h)
print("################date ohlc updown###########################")
code = sys.argv[1]
date = int(sys.argv[2])

#ss = ef.stock.get_realtime_quotes(['美股'])
#print(ss)
#date = '20250208'
#date2 = '20250308'
#code = 'TSLA'
ns = ef.stock.get_quote_history(code, beg = date)#, end = date2)
print(ns['日期'].values.tolist())

ns['日期'] = pd.to_datetime(ns['日期'], errors='coerce')
ns['日期'] = ns['日期'].apply(lambda x: datetime.datetime.timestamp(x))
ns['日期'] = ns['日期'].apply(lambda x: int(round(x * 1000)))
ohlc = (ns[['日期', '开盘', '最高', '最低', '收盘']].values.tolist()) #ohlc
updown = ns[['日期', '涨跌额']].values.tolist()
print(ohlc)
print(updown)
max_values = ns.max()
mx = (max_values['最高'])
min_values = ns.min()
mn = (min_values['最低'])
rate = (mn - mx) / mx * 100.0
rate = ' ' + str(rate) + '%' if rate < 0 else ' +' + str(rate) + '%' 

print("################high low rate###########################")
print(code, mx, mn, rate)
sys.exit("\n\t\tcontinue trade? connect to app...")