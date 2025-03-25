import efinance as ef
# https://stockanalysis.com/quote/hkg/7552/chart/
# write a boduan
stock_code = '07552'; stockavg = 1.902; zgs = 33.62# yi
st = '20250226'
et  = '20250325'

from datetime import datetime
date1 = datetime.strptime(st, "%Y%m%d")
date2 = datetime.strptime(et, "%Y%m%d")

# Calculate the difference between the two dates
delta = date2 - date1

# Extract the number of days from the difference
number_of_days = delta.days

df = ef.stock.get_quote_history(stock_code, beg = st, end= et, klt = 101)
#left = df.tail(5).iloc[:, [1, 2,3]]
#print(left.to_markdown(numalign="left", stralign="left"))
#print(df.columns)
d = [0, 2, 4, 5, 6]


left = df.iloc[:, d]
#print(left.to_csv(index=False))
trade_of_days = left.shape[0]


#left = df.tail(days).iloc[:, d]
#s = (left.to_string())
#for i in s.split('\n'): print(i.split(' '))

#s = (left.to_string())
#for i in s.split('\n'): print(i.split(' '))
print (left)

m = left.iloc[:, 2].mean()
avg = m
#print ("avg close", avg)
print()


print ("min price")
mx = (left.iloc[:, 4].min())
print(mx)
t = left.iloc[:, 4]==mx
print (left[t])
print()

print ("max price")
mx = (left.iloc[:, 3].max())
print(mx)
t = left.iloc[:, 3]==mx
print (left[t])
print()


d = [0, 2, 7, 8, 11, 12]
left = df.iloc[:, d]


mn = (left.iloc[:, 2].min())
t = left.iloc[:, 2]==mn
#date = (left[t].iloc[:, 1].to_string(index=False))
print ("min trade")
print (left[t].iloc[:, [0, 1, 2, 4, 5]])
print()

mx = (left.iloc[:, 2].max())
t = left.iloc[:, 2]==mx
#date = (left[t].iloc[:, 1].to_string(index=False))
print ("max trade")
print (left[t].iloc[:, [0, 1, 2, 4, 5]])
print()


print(f"days between {st} and {et}: {number_of_days}")
print(f"trade between {st} and {et}: {trade_of_days}")
m = left.iloc[:, 3] / left.iloc[:, 2]  
mm = m.mean()
print ("people vwmp:", mm)
mx = (m.min())
t = left.iloc[:, 3] / left.iloc[:, 2]  ==mx
#date = (left[t])
#date = (left[t].iloc[:, 1].to_string(index=False))
date = (left[t].iloc[:, [1, 4, 5]].to_string(index=False, header = None))
print ("buy at min vwmp?", date, "^ ^")

mx = (left.iloc[:, 2].max())
t = left.iloc[:, 2]==mx
#date = (left[t])
#date = (left[t].iloc[:, 1].to_string(index=False))
date = (left[t].iloc[:, [1, 4, 5]].to_string(index=False, header = None))
print ("sell at max turn?", date)
print (">>>> ma", avg, "\n>>>> me", stockavg)

dl = df["成交量"].to_list()
print ('总股数', zgs, '亿')
print ('一半是', zgs*100000000/10000*0.5, '万')
result = [x / 10000.0 for x in dl]
print ('成交量', result, '万')

l = len(result)+1
for i in range (1, l): 
    s = sum(result[0:i])
    print('累积量', s, '的1/3是主力', 1/3*s)
#print (sum(result))
# = left.iloc[:, 2].mean()


df["pvt"] = df["收盘"] * df["成交量"] 
df["vwap"] = df["pvt"].cumsum() / df["成交量"].cumsum()

#print(df[["涨跌额", "收盘", "vwap"]])
print("=>=> vwap min", df["vwap"].min())
qian = df.sort_values(by='涨跌额', ascending=False)
print ("=>=> avg up", qian["涨跌额"].mean())
print ("=>=> max up", qian["涨跌额"].max())

qt=(qian.tail(7)[['日期', '收盘', "涨跌额", "成交量", "vwap"]])
#['股票名称', '股票代码', '日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅','涨跌额', '换手率'],
s = (qt.to_csv())
print("id", s)
#for i in s.split('\n'): print(i.split(' '))
print("orgnization cost =>", qt['vwap'].mean())