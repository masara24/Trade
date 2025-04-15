import efinance as ef
import sys
# https://stockanalysis.com/quote/hkg/7552/chart/
h = "python signal.py 07552 1" #from 2 to 14
if len(sys.argv)-1 !=2: sys.exit(h)
print("################1 : 分钟 5 : 5 分钟 15 : 15 分钟 30 : 30 分钟 60 : 60 分钟 101 : 日 102 : 周 103 : 月###########################")

code = sys.argv[1]
klt = sys.argv[2]
# day = today
hb = ef.stock.get_today_bill(code )

qh = ef.stock.get_quote_history(code, klt)

import pandas as pd

#import datetime
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.float_format', lambda x: '%16.3f' % x)


merged_df = pd.merge(hb, qh, how='inner')

merged_df['流入'] = merged_df['小单净流入']+merged_df['中单净流入']+merged_df['大单净流入']+merged_df['超大单净流入']
#merged_df['涨跌额']



sp = merged_df['收盘'].values.tolist()
import numpy as np
zsp = [np.nan] + sp[:-1]
merged_df.insert(2, "昨收盘", zsp, True)

merged_df['今开减昨收'] = merged_df['开盘'] - merged_df['昨收盘']
merged_df['今收减今开'] = merged_df['开盘'] - merged_df['收盘']
merged_df['最低减最高'] = merged_df['最低'] - merged_df['最高']

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
k = ef.stock.get_top10_stock_holder_info(code, top = 1)
print(k)
info = pd.DataFrame({'数据': data})

info_html = info.to_html(classes='table')


html = '''<html>
<head>
<meta charset="gbk" />
<title>pandas</title>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/treemap.js"></script>
<script src="https://code.highcharts.com/modules/treegraph.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
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

    <button onclick="mergeTables()">某种质朴的决策树</button>
    <button onclick="predictTables()" style="background-color: green; color: white;">某种神奇的预测术</button>
    <button onclick="removeTables()">移除新生成的表格</button>

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




