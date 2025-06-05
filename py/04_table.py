import efinance as ef
import sys
# https://stockanalysis.com/quote/hkg/7552/chart/
h = "python table.py 07500@2.6 2025-02-01to2025-06-05" #from 2 to 14
if len(sys.argv)-1 !=2: sys.exit(h)
print("################date volume###########################")

stock = sys.argv[1]
dates = sys.argv[2]
code, zgs = stock.split('@')
zgs = float(zgs)
date, date2 = dates.split('to')

ss = ef.stock.get_history_bill(code)
hb = ss[(ss['日期'] >= date) & (ss['日期'] <= date2)].copy() 
hb['日期'] = hb['日期'].apply(lambda x: x + ' 16:00')

ss = ef.stock.get_quote_history(code)
qh = ss[(ss['日期'] > date) & (ss['日期'] < date2)].copy() 
qh['日期'] = qh['日期'].apply(lambda x: x + ' 16:00')

import pandas as pd

#import datetime
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.float_format', lambda x: '%16.3f' % x)


merged_df = pd.merge(hb, qh, how='inner')


from datetime import datetime
st = datetime.strptime(date, "%Y-%m-%d")
et = datetime.strptime(date2, "%Y-%m-%d")

# Calculate the difference between the two dates
delta = et - st

# Extract the number of days from the difference
number_of_days = delta.days

trade_of_days = merged_df.shape[0]

print(f"days between {st} and {et}: {number_of_days}")
print(f"trade between {st} and {et}: {trade_of_days}")

merged_df['流入'] = merged_df['小单净流入']+merged_df['中单净流入']+merged_df['大单净流入']+merged_df['超大单净流入']
#merged_df['涨跌额']



sp = merged_df['收盘'].values.tolist()
import numpy as np
zsp = [np.nan] + sp[:-1]
merged_df.insert(2, "昨收盘", zsp, True)

merged_df['今开减昨收'] = merged_df['开盘'] - merged_df['昨收盘']
merged_df['今收减今开'] = merged_df['开盘'] - merged_df['收盘']
merged_df['最低减最高'] = merged_df['最低'] - merged_df['最高']

#成交量
dt = merged_df["日期"].to_list() + ['最终累计']

dl = merged_df["成交量"].to_list()
print ('总股数', zgs, '亿')
print ('一半是', zgs*100000000/10000*0.5, '万')
result = [x / 10000.0 for x in dl]
print ('成交量', result, '万')

l = len(result)+1
for i in range (1, l): 
    s = sum(result[0:i])
    
    if s > zgs*100000000/10000*0.5: print(dt[i], '累积量', s, '的1/3是主力', 1/3*s, '>>控盘<<')
    else: print(dt[i], '累积量', s, '的1/3是主力', 1/3*s)
#print (sum(result))
# = left.iloc[:, 2].mean()


merged_df["pvt"] = merged_df["收盘"] * merged_df["成交量"] 
merged_df["vwap"] = merged_df["pvt"].cumsum() / merged_df["成交量"].cumsum()
print("################avg updown###########################")

#print(df[["涨跌额", "收盘", "vwap"]])
print("=>=> vwap min", merged_df["vwap"].min())
qian = merged_df.sort_values(by='涨跌额', ascending=False)
print ("=>=> avg updown", qian["涨跌额"].mean())
print ("=>=> max updown", qian["涨跌额"].max())

# kdj
low_list=merged_df['最低'].rolling(window=9).min()
low_list.fillna(value=merged_df['最低'].expanding().min(), inplace=True)
high_list = merged_df['最高'].rolling(window=9).max()
high_list.fillna(value=merged_df['最高'].expanding().max(), inplace=True)

rsv = (merged_df['收盘'] - low_list) / (high_list - low_list) * 100
merged_df['KDJ_K'] = rsv.ewm(com=2).mean()
merged_df['KDJ_D'] = merged_df['KDJ_K'].ewm(com=2).mean()
merged_df['KDJ_J'] = 3 * merged_df['KDJ_K'] - 2 * merged_df['KDJ_D']

merged_df['KDJ_金叉死叉'] = ''
kdj_position = merged_df['KDJ_K'] > merged_df['KDJ_D']
merged_df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉，买'
merged_df.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉，卖'


#macd
merged_df['EMA12'] = merged_df['收盘'].ewm(span=12, adjust=False).mean()
merged_df['EMA_long'] = merged_df['收盘'].ewm(span=26, adjust=False).mean()

merged_df['DIF'] = merged_df['EMA12'] - merged_df['EMA_long'] # fast - slow

merged_df['DEA'] = merged_df['DIF'].ewm(span=9, adjust=False).mean() # 

merged_df['MACD'] = 2 * (merged_df['DIF'] - merged_df['DEA']) # histo

merged_df['macd_金叉死叉'] = ''
macd_position = merged_df['DIF'] > merged_df['DEA']
merged_df.loc[macd_position[(macd_position == True) & (macd_position.shift() == False)].index, 'macd_金叉死叉'] = '金叉，买'
merged_df.loc[macd_position[(macd_position == False) & (macd_position.shift() == True )].index, 'macd_金叉死叉'] = '死叉，卖'

merged_df['5日穿10日'] = ''
merged_df['m5'] = merged_df['收盘'].rolling(window=5).mean().dropna()  
merged_df['m10'] = merged_df['收盘'].rolling(window=10).mean().dropna()
ma_position = merged_df['m5'] > merged_df['m10']
merged_df.loc[ma_position[(ma_position == True) & (ma_position.shift() == False)].index, '5日穿10日'] = '上，买'
merged_df.loc[ma_position[(ma_position == False) & (ma_position.shift() == True)].index, '5日穿10日'] = '下，卖'

merged_df = merged_df[['日期', '收盘', '成交量', '昨收盘', '开盘', '今开减昨收', '今收减今开', '最低', '最高', '流入', 'KDJ_J', 'KDJ_金叉死叉', 'EMA12', 'macd_金叉死叉', 'm10', '5日穿10日']]
merged_html = merged_df.to_html(classes='table')

data = {'说明': ['总股本', ' 总流通', '股息ttm', '分红', 'beta'],
'数据': [np.nan]*5}
#6.98e8, 2.91e8, 1.78, 0.5, 0]}
info = pd.DataFrame(data)


data = ef.stock.get_base_info(code)
#k = ef.stock.get_top10_stock_holder_info(code, top = 1)
#print(k)
info = pd.DataFrame({'数据': data})

info_html = info.to_html(classes='table')


html = '''<html>
<head>
<meta charset="gbk" />
<title>pandas</title>
<script src="https://code.highcharts.com/highcharts.js"></script>

<style>
  .flex-container {
    display: flex;
  }

  .flex-item {
    flex: 1;
  }

table {
  margin: 10px; /* 为表格之间创建一定的间距 */
  border: 1px solid black; /* 添加表格边框 */
word-break: keep-all;//break-all;
}

table, th, td {
  border: 1px solid black;
}

th, td {
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #FFDE59;
}

td:hover {
  background-color: #98F5F9;
}
</style>

</head>
<body><center><div><h3>''' + code + '''</h3>
''' + info_html + '''

    <button onclick="mergeTables()">流入计算</button>
    <button onclick="predictTables()" style="background-color: green; color: white;">价格预测</button>
    <button onclick="removeTables()">恢复正常</button>

<div id="hide">


</div></div>

<div class="flex-container">
<div class="flex-item">''' + merged_html + '''

</div>
</div>



</center>



</body>
</html>'''


with open(f'{code}.html', 'w') as f: f.write(html)

import os 
os.startfile(f'{code}.html')




