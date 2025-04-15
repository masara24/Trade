import efinance as ef
import sys
#pip install tabulate
h = "python benefit.py 07552 1.95"
if len(sys.argv)-1 !=2: sys.exit(h)

stock_code = sys.argv[1]
stockavg = float(sys.argv[2])
print("################date max min###########################")

d = [0, 2, 4, 5, 6, 7]
#['股票名称', '股票代码', '日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅','涨跌额', '换手率'],
df = ef.stock.get_quote_history(stock_code)
days = 7
days = 15 # buy 2 weeks ago
print ("days", days)
left = df.tail(days).iloc[:, d]
print (left.to_markdown(
        numalign="left",
        stralign="left",
    ))

m = left.iloc[:, 2].mean()
avg = m
#print ("avg close", avg)
print()
print ("max price")
xmx = (left.iloc[:, 3].max())
#print(xmx)
t = left.iloc[:, 3]==xmx
print (left[t])
print()

print ("min price")
xmn = (left.iloc[:, 4].min())
#print(xmn)
t = left.iloc[:, 4]==xmn
print (left[t])
print()

d = [0, 2, 7, 8, 11, 12]
left = df.tail(days).iloc[:, d]

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

m = left.iloc[:, 3] / left.iloc[:, 2]  
mm = m.mean()
#print ("avg vwmp", mm)

mx = (m.min())
t = left.iloc[:, 3] / left.iloc[:, 2]  ==mx
#date = (left[t])
date = (left[t].iloc[:, 1].to_string(index=False))
#date = (left[t].iloc[:, [1, 4, 5]].to_string(index=False, header = None))
print ("buy at min vwmp", date, '\n', df.loc[df['日期']==date].to_string(index=False, header = None))
print()
mx = (left.iloc[:, 2].max())
t = left.iloc[:, 2]==mx
#date = (left[t])
date = (left[t].iloc[:, 1].to_string(index=False))
#date = (left[t].iloc[:, [1, 4, 5]].to_string(index=False, header = None))
print ("sell at max turn", date, '\n', df.loc[df['日期']==date].to_string(index=False, header = None))
print()
print("################price compare###########################")


print ("max =>", xmx)
print ("avg =>", avg)
print("min =>", xmn)


print("my cost =>", stockavg, "hold days", days)

print("people =>", mm)


sys.exit("\n\t\tcontinue trade? connect to app...")


