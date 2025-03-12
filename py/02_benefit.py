import pandas as pd
import sys

h = "python df_benefit.py -10@9.8,-10@12,20@13 1"
if len(sys.argv)-1 !=2: sys.exit(h)
print("################market 1 = us, 2 = hk, 3 = etf ###########################")

yourinput = sys.argv[1]
market = int(sys.argv[2])

dict = {
    "trade": ["quantity@price"],
    "fee": [0],
    "waste": [0],
    "quantity": [0],
    "#assets": [0],
    "costs": [0],
    "avg": [0],
    "cash": [0],
    "benefit": "percentage",
}
df = pd.DataFrame(dict)
assets = 0
quantity = 0
costs = 0
waste = 0
benefit = "0%"
cash = 0
times = 0

last = {
    "trade": [""],
    "fee": [0],
    "waste": [0],
    "quantity": [0],
    "#assets": [0],
    "costs": [0],
    "avg": [0],
    "cash": [0],
    "benefit": "",
}

import math
def payus(qty, prc): # for number

    #print("payus for kong")

    pos = abs(qty)
    a = pos * 0.0049 if pos * 0.0049 >= 0.99 else 0.99
    a = a if a <= pos * prc * 0.5 * 0.01 else pos * prc * 0.5 * 0.01
    b = pos * 0.005 if pos * 0.005 >= 1 else 1
    b = b if b <= pos * prc * 0.5 * 0.01 else pos * prc * 0.5 * 0.01
    c = 0.003 * pos
    d = 0
    e = 0
    if qty < 0:
        d = 0.0000278 * prc * pos; d = 0.01 if d <= 0.01 else d; e = 0.000166 * pos; e = 8.3 if d >= 8.3 else d; e = 0.01 if d <= 0.01 else d
    fee = a + b + c + d + e
    print("US", a, b, c, d, e)

    fee = math.ceil(fee * 100) / 100
    return fee


def payhk(pos):

    #print("payhk for duo")

    a = pos * 0.03 * 0.01 if pos * 0.03 * 0.01 >= 3 else 3
    b = 15
    c = 0.002 * 0.01 * pos
    c = c if c >= 2 else 2
    c = c if c <= 100 else 100
    d = math.ceil(0.1 * 0.01 * pos)
    e = 0.00565 * 0.01 * pos if 0.00565 * 0.01 * pos >= 0.01 else 0.01
    f = 0.0027 * 0.01 * pos if 0.0027 * 0.01 * pos >= 0.01 else 0.01
    g = 0.00015 * 0.01 * pos
    fee = a + b + c + d + e + f + g
    print("HK", a, b, c, d, e, f, g)
    fee = math.ceil(fee * 100) / 100
    return fee

def payhketf(pos):

    #print("payhk for duo")

    a = pos * 0.03 * 0.01 if pos * 0.03 * 0.01 >= 3 else 3
    b = 15
    c = 0.002 * 0.01 * pos
    c = c if c >= 2 else 2
    c = c if c <= 100 else 100
    d = 0#math.ceil(0.1 * 0.01 * pos)
    e = 0.00565 * 0.01 * pos if 0.00565 * 0.01 * pos >= 0.01 else 0.01
    f = 0.0027 * 0.01 * pos if 0.0027 * 0.01 * pos >= 0.01 else 0.01
    g = 0.00015 * 0.01 * pos
    fee = a + b + c + d + e + f + g
    print("HK", a, b, c, d, e, f, g)
    fee = math.ceil(fee * 100) / 100
    return fee


def call(market):
    print("################estimate call with fee###############################")
    transaction = yourinput.split(",")
    aptab = ""
    aplst = []
    avgprc = [0]

    for i in transaction:
        q, p = i.split("@")
        global waste; global costs; global cash; global assets; global df; global quantity; global last; global times
        aplst.append([q, p])
        times = times + 1
        if q[0] == "-":
            T = q[1:].isnumeric() and p.replace(".", "0").isnumeric()
        else:
            T = q.isnumeric() and p.replace(".", "0").isnumeric()
        if T:

            trade = float(p) * int(q)  # postive if buy, negtive if sell
            pos = abs(trade)
            #fee = payus(int(q), float(p))
            if market == 1: fee = payus(int(q), float(p))  # but fee is always postive, and postive means spent
            if market == 2: fee = payhk(pos)  # but fee is always postive, and postive means spent
            if market == 3: fee = payhketf(pos)  # but fee is always postive, and postive means spent
            waste = waste + fee
            assets = assets + float(p) * (int(q))
            quantity = quantity + (int(q))
            
            cash = cash + trade + fee
            if trade > 0:
                costs = costs + trade + fee

            else:
                costs = costs + fee

            if quantity == 0:
                avg = 0; assets = 0; avgprc.append(0)
            else:

                if cash < 0:
                    avg = (assets + fee) / quantity
                else:
                    avg = (costs) / quantity; avgprc.append((assets + 0) / quantity)

            print("compare to no fee", avgprc)
            if costs != 0:
                benefit = f"{-cash / costs:.2%}"

            last = {
                "trade": i,
                "fee": fee,
                "waste": waste,
                "quantity": quantity,
                "#assets": assets,
                "costs": costs,
                "avg": avg,
                "cash": -cash,
                "benefit": benefit
            }

            df = df._append(last, ignore_index=True)

        else:
            aptab = aptab + (f"| {times}  | {q} @ {p}\n")

    gfg = df.to_markdown(
        numalign="left",
        stralign="left",
    )

    print(gfg)

def put(market):
    print("################estimate put with fee###############################")
    transaction = yourinput.split(",")

    aptab = ""
    aplst = []
    avgprc = [0]
    for n, i in enumerate(transaction):
        q, p = i.split("@")
        global waste; global costs; global cash; global assets; global df; global quantity; global last; global times

        aplst.append([q, p])
        times = times + 1
        buyq = int(q)
        buyp = float(p)
        quantity = quantity - buyq        

        trade = buyq * buyp  # postive if sell negtive if buy
        pos = abs(trade)
        if market == 1: fee = payus(int(q), float(p))  # but fee is always postive, and postive means spent
        if market == 2: fee = payhk(pos)  # but fee is always postive, and postive means spent
        if market == 3: fee = payhketf(pos)  # but fee is always postive, and postive means spent
        waste = waste + fee
        assets = assets - trade
        
        if quantity == 0:  # this is the ending point
            avg = 0; assets = 0; avgprc.append(0)

        else:
            avg = (assets + waste) / quantity; avgprc.append(((assets + 0) / quantity))

        print("compare to no fee", avgprc)
        if trade < 0:
            costs = costs + trade - fee
            cash = cash + trade - fee

        else:
            costs = costs - fee

            cash = buyq * (avgprc[-2] - buyp) - fee # oh, the cash not useful here
            #print(buyq, avgprc[-2]- buyp, cash)


        if costs != 0:
            benefit = f"{-cash / costs:.2%}"

        last = {
            "trade": i,
            "fee": fee,
            "waste": waste,
            "quantity": quantity,
            "#assets": -assets,
            "costs": -costs,
            "avg": avg,
            "cash": cash,
            "benefit": benefit,
        }

        df = df._append(last, ignore_index=True)
    gfg = df.to_markdown(
        numalign="left",
        stralign="left",
    )
    # df.to_excel("save.xlsx", sheet_name='save')
    print(gfg)


if yourinput[0] == "-": put(market)
else: call(market)

sys.exit("\n\t\tcontinue akshare? connect to internet...")

