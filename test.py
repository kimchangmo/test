#김창모
#api키 : Xe70g6uznpnBznhPBKPUBfY5pB52kvH0o7aqFiJsYN6ZxKtyxONAsMgNhI0JVOv6
#비밀키 : RMgRWgyHizGLqdF7P2wf8LeajnewCHMjMLLrDR5nL2651324ulQ0DotI6l5RqMJV

#아빠
#api키 : 9IcrYyV1ckCJMMrCLDoIUFNG77e86szaM0mW7jpO3evAHjLJXZfGORejbEmStRjh
#비밀키 : sjZCJF5YRzPm5qaSy91IPjK7qz9a65VCfn7wmw0ji7AQJndPnUYZo8dLAjs2ceCt

#참고 : 
#pip install ccxt 
#pip install binance-connector 
#pip install --upgrade pip 
#pip install python-binance 
#pip install binance-futures 

#윈도우만 참고:
#시간설정 time.nist.gov 로 변경! 
#시계 자동 동기화 적용 할것!!!

#-----------테스트코드--------------------------------------------------------------------------
import ccxt 
import time
import pandas as pd
from datetime import datetime, timezone
from binance.spot import Spot as Client
from binance.client import Client as r_Client
import datetime as dt

#키
api_key = "Xe70g6uznpnBznhPBKPUBfY5pB52kvH0o7aqFiJsYN6ZxKtyxONAsMgNhI0JVOv6"
secret  = "RMgRWgyHizGLqdF7P2wf8LeajnewCHMjMLLrDR5nL2651324ulQ0DotI6l5RqMJV"

print('##################################Start############################################')

binance = ccxt.binance(config={
    'apiKey': api_key, 
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

#선물잔고조회
balance = binance.fetch_balance(params={"type": "future"})
print('선물잔고 :', balance['USDT'])

def rsi(symbol):
    #특정코인 과거데이터 조회
    client = Client(api_key, secret)

    klines = client.klines(symbol, '30m', limit=500)

    df = pd.DataFrame(data={
        'open_time': [datetime.fromtimestamp(x[0] / 1000, timezone.utc) for x in klines],
        'open': [float(x[1]) for x in klines],
        'high': [float(x[2]) for x in klines],
        'low': [float(x[3]) for x in klines],
        'close': [float(x[4]) for x in klines],
        'volume': [float(x[5]) for x in klines],
        'close_time': [datetime.fromtimestamp(x[6] / 1000, timezone.utc) for x in klines],
    })

    #rsi 구하는놈
    closedata = df["close"]
    delta = closedata.diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    period = 14 
    au = ups.ewm(com = period-1, min_periods = period).mean() 
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = au/ad 

    return pd.Series(100 - (100/(1 + RS)), name = "RSI")
 
#코인목록
all_coin = []
markets = binance.load_markets()
for m in markets:
    usdt = 'USDT' in m
    if usdt:
        new_m = m.replace('/','')
        all_coin.append(new_m)

#롱 and 숏 몇개 돌릴건지 설정
#coin_buy_index = 1
coin_buy_index = 20
#분봉 +2
delay_time = 32
#보유머니의 1/n시작
nmoney = 400
#배율
all_leverage = 5

for n in range(0, coin_buy_index):
    #코인별 롱/숏 보유상태
    globals()['count_buy_{}'.format(n)] = 'true'
    globals()['count_sell_{}'.format(n)] = 'true'
    #globals()['coin_{}'.format(n)] = all_coin[i]





# coin = 'RAYUSDT'
# print('코인:', coin)


# #########최대 구매량 구하는 공식###########
# client = r_Client(api_key=api_key, api_secret=secret)
# info = client.futures_exchange_info()
# maxQty = [coin]
# maxQty = {si['symbol']:si['filters'] for si in info['symbols'] if si['symbol'] in maxQty}
# maxQty = maxQty[coin]
# maxQty = maxQty[2]
# maxQty = float(maxQty['maxQty'])
# print('최대구매량:', maxQty)
# print('코인가격:', float(client.futures_symbol_ticker(symbol=coin)['price']))


# #########구매량 계산#########
# balance = binance.fetch_balance(params={"type": "future"})
# first_buy_money = balance['USDT']['free'] + balance['USDT']['used']
# first_buy_money = int(first_buy_money/nmoney)
# purchasing_volume = first_buy_money*all_leverage/float(client.futures_symbol_ticker(symbol=coin)['price'])


# #물타기 성공 횟수(테스트용)
# n = 0
# #몇번 나눠서 구매해야 하는지 변수 > 최초 구매시 초기화 하고 물타기시엔 초기화 X
# Number_of_Divisions = 1

# while True:
#     if maxQty > purchasing_volume :
#         #구매
#         # client.futures_create_order(
#         #     symbol=coin, side='BUY',
#         #     positionSide = 'LONG', type='MARKET', quantity=round(globals()['buy_money_{}'.format(n)],decimal_point)
#         # )
#         print('구매량:', purchasing_volume)
#         print('물타기 ', n, '번째 성공')
#         print('-----------------------------------------')
#         purchasing_volume = purchasing_volume*2
#         divisions_purchasing_volume = purchasing_volume
#         n = n+1
#     else :
#         for x in range(0, Number_of_Divisions):
#             #최대수량보다 구매수량이 클 경우 나눌 횟수 계산
#             if maxQty < divisions_purchasing_volume :
#                 Number_of_Divisions = Number_of_Divisions*2
#                 print(Number_of_Divisions, '번 나눔')
#                 divisions_purchasing_volume = purchasing_volume/Number_of_Divisions
#                 print(Number_of_Divisions, '번 나눈 구매량:', divisions_purchasing_volume)
#                 print('-----------------------------------------')
#             else :
#                 #구매
#                 # client.futures_create_order(
#                 #     symbol=coin, side='BUY',
#                 #     positionSide = 'LONG', type='MARKET', quantity=round(globals()['buy_money_{}'.format(n)],decimal_point)
#                 # )
#                 print('구매량:', purchasing_volume)
#                 print(divisions_purchasing_volume, '의 수량으로 ', Number_of_Divisions, '번 나눠 구매 성공')
#                 print('물타기 ', n, '번째 성공')
#                 print('-----------------------------------------')
#                 purchasing_volume = purchasing_volume*2
#                 divisions_purchasing_volume = purchasing_volume
#                 n = n+1
#                 break
    
#     time.sleep(3)



while True:
    i = 0

    #코인목록
    all_coin = []
    markets = binance.load_markets()
    for m in markets:
        usdt = 'USDT' in m
        if usdt:
            new_m = m.replace('/','')
            all_coin.append(new_m)

    while i < len(all_coin) : #총 코인 갯수
        try:
            coin = all_coin[i]
            now_rsi = float(rsi(coin).iloc[-1])
            old_rsi = float(rsi(coin).iloc[-2])
            old_old_rsi = float(rsi(coin).iloc[-3])
            now = dt.datetime.now()

            #선물잔고조회
            balance = binance.fetch_balance(params={"type": "future"})
            #잔고에 따른 구매액수 변환
            first_buy_money = balance['USDT']['free'] + balance['USDT']['used']
            first_buy_money = int(first_buy_money/nmoney)
                    
            #모든 코인구매칸이 다찼는지 확인
            for n in range(0, coin_buy_index):
                if (globals()['count_buy_{}'.format(n)] == 'false'):
                    count_all_buy = 'false'
                else:
                    count_all_buy = 'true'
                    break
            for n in range(0, coin_buy_index):
                if (globals()['count_sell_{}'.format(n)] == 'false'):
                    count_all_sell = 'false'
                else:
                    count_all_sell = 'true'
                    break


############코인 롱 구매###############
            #if (30 > old_old_rsi) and (30 < old_rsi) and (30 < now_rsi) and (count_all_buy == 'true'):
            if True:
                for n in range(0, coin_buy_index):
                    #보유여부확인
                    positions = balance['info']['positions']
                    for position in positions:
                        if (position["symbol"] == coin) and (float(position["initialMargin"]) > 0) and (position["positionSide"] == "LONG") :
                            live_buy_coin = 'false'
                            break
                        if (position["symbol"] == coin) and (float(position["initialMargin"]) == 0) and (position["positionSide"] == "LONG") :
                            live_buy_coin = 'true'
                            break

                    if (globals()['count_buy_{}'.format(n)] == 'true') and (live_buy_coin == 'true'):
                        #선물잔고조회
                        balance = binance.fetch_balance(params={"type": "future"})
                        #구매수량 계산 - 구매가*배율/코인가격
                        client = r_Client(api_key=api_key, api_secret=secret)
                        globals()['buy_money_{}'.format(n)] = first_buy_money*all_leverage/float(client.futures_symbol_ticker(symbol=coin)['price'])

                        #quantity 자리수 설정
                        client = r_Client(api_key=api_key, api_secret=secret)
                        info = client.futures_exchange_info()
                        requestedFutures = [coin]
                        decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                        decimal_point = decimal_point.replace('{', '')
                        decimal_point = decimal_point.replace('}', '')
                        #아래 값을 round 에서 사용하면 됨
                        decimal_point = int(decimal_point)
                        
                        if (first_buy_money < balance['USDT']['free']):
                            print('try buy(long) :', coin)
                            client = r_Client(api_key=api_key, api_secret=secret)
                            #레버리지 설정
                            client.futures_change_leverage(symbol = coin, leverage = all_leverage)
                            #구매
                            client.futures_create_order(
                                symbol=coin, side='BUY',
                                positionSide = 'LONG', type='MARKET', quantity=round(globals()['buy_money_{}'.format(n)],decimal_point)
                            )
                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']
                            for position in positions:
                                if (position["symbol"] == coin) and (position["positionSide"] == "LONG"):
                                    print('entry',position['entryPrice'])
                                    entry = position['entryPrice']
                                    break

                            globals()['last_buy_money_{}'.format(n)] = first_buy_money
                            globals()['price_buy_{}'.format(n)] = client.futures_symbol_ticker(symbol=coin)
                            globals()['water_buy_price_buy_{}'.format(n)] = float(entry)
                            globals()['last_current_price_buy_{}'.format(n)] = float(globals()['price_buy_{}'.format(n)]['price'])
                            globals()['buycoin_buy_{}'.format(n)] = coin
                            #물타는 지점 점진적 증가
                            globals()['increase_water_buy_{}'.format(n)] = 0.95

                            #구매시간
                            globals()['buytime_buy_{}'.format(n)] = dt.datetime.now() + dt.timedelta(minutes=delay_time)
                            globals()['buy_money_buy_{}'.format(n)] = globals()['buy_money_{}'.format(n)]
                            globals()['old_plus_buy_{}'.format(n)] = globals()['buy_money_{}'.format(n)]

                            globals()['count_buy_{}'.format(n)] = 'false'
                            print('time :', now)
                            print('success buy coin(long) :', coin)
                            print('----------------------------------------------------')
                            time.sleep(1000)    
                            break

############코인 숏 구매############
            #if (70 < old_old_rsi) and (70 > old_rsi) and (70 > now_rsi) and (count_all_sell == 'true'):
            if False:
                for n in range(0, coin_buy_index):
                    #보유여부확인
                    positions = balance['info']['positions']
                    for position in positions:
                        if (position["symbol"] == coin) and (float(position["initialMargin"]) > 0) and (position["positionSide"] == "SHORT") :
                            live_sell_coin = 'false'
                        if (position["symbol"] == coin) and (float(position["initialMargin"]) == 0) and (position["positionSide"] == "SHORT") :
                            live_sell_coin = 'true'
                    if (globals()['count_sell_{}'.format(n)] == 'true') and (live_sell_coin == 'true'):
                        #선물잔고조회
                        balance = binance.fetch_balance(params={"type": "future"})
                        #구매수량 계산 - 구매가*배율/코인가격
                        client = r_Client(api_key=api_key, api_secret=secret)
                        globals()['buy_money_{}'.format(n)] = first_buy_money*all_leverage/float(client.futures_symbol_ticker(symbol=coin)['price'])

                        #quantity 자리수 설정
                        client = r_Client(api_key=api_key, api_secret=secret)
                        info = client.futures_exchange_info()
                        requestedFutures = [coin]
                        decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                        decimal_point = decimal_point.replace('{', '')
                        decimal_point = decimal_point.replace('}', '')
                        decimal_point = int(decimal_point)

                        if (first_buy_money < balance['USDT']['free']) :
                            print('try buy(short) :', coin)
                            client = r_Client(api_key=api_key, api_secret=secret)          
                            #레버리지 설정
                            client.futures_change_leverage(symbol = coin, leverage = all_leverage)
                            #구매
                            client.futures_create_order(
                                symbol=coin, side='SELL',
                                positionSide = 'SHORT', type='MARKET', quantity=round(globals()['buy_money_{}'.format(n)],decimal_point)
                            )
                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']
                            for position in positions:
                                if (position["symbol"] == coin) and (position["positionSide"] == "SHORT"):
                                    print('entry',position['entryPrice'])
                                    entry = position['entryPrice']
                                    break

                            globals()['last_sell_money_{}'.format(n)] = first_buy_money
                            globals()['price_sell_{}'.format(n)] = client.futures_symbol_ticker(symbol=coin)
                            globals()['water_buy_price_sell_{}'.format(n)] = float(entry)
                            globals()['last_current_price_sell_{}'.format(n)] = globals()['price_sell_{}'.format(n)]['price']
                            globals()['buycoin_sell_{}'.format(n)] = coin
                            #물타는 지점 점진적 증가
                            globals()['increase_water_sell_{}'.format(n)] = 1.05

                            #구매시간
                            globals()['buytime_sell_{}'.format(n)] = dt.datetime.now() + dt.timedelta(minutes=delay_time)
                            globals()['buy_money_sell_{}'.format(n)] = globals()['buy_money_{}'.format(n)]
                            globals()['old_plus_sell_{}'.format(n)] =globals()['buy_money_{}'.format(n)]

                            globals()['count_sell_{}'.format(n)] = 'false'
                            print('time :', now)
                            print('success buy coin(short) :', coin)
                            print('----------------------------------------------------')
                            time.sleep(1)    
                            break


            for n in range(0, coin_buy_index):
                #수동판매 대응
                balance = binance.fetch_balance(params={"type": "future"})
                positions = balance['info']['positions']
                for position in positions:
                    if (globals()['count_buy_{}'.format(n)] == 'false') and (position["symbol"] == globals()['buycoin_buy_{}'.format(n)]) and (float(position["initialMargin"]) == 0) and (position["positionSide"] == "LONG") :
                        globals()['count_buy_{}'.format(n)] = 'true'
                    if (globals()['count_sell_{}'.format(n)] == 'false') and (position["symbol"] == globals()['buycoin_sell_{}'.format(n)]) and (float(position["initialMargin"]) == 0) and (position["positionSide"] == "SHORT") :
                        globals()['count_sell_{}'.format(n)] = 'true'

                if (globals()['count_buy_{}'.format(n)] == 'false'):
                    #코인 현재가(롱)
                    client = r_Client(api_key=api_key, api_secret=secret)
                    globals()['current_price_buy_{}'.format(n)] = client.futures_symbol_ticker(symbol=globals()['buycoin_buy_{}'.format(n)])
                    globals()['current_price_buy_{}'.format(n)] = float(globals()['current_price_buy_{}'.format(n)]['price'])
                    
####################1퍼 익절(롱)####################
                    if ((float(globals()['water_buy_price_buy_{}'.format(n)]) * 1.01) < globals()['current_price_buy_{}'.format(n)]) :

                        #quantity 자리수 설정
                        client = r_Client(api_key=api_key, api_secret=secret)
                        info = client.futures_exchange_info()
                        requestedFutures = [globals()['buycoin_buy_{}'.format(n)]]
                        decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                        decimal_point = decimal_point.replace('{', '')
                        decimal_point = decimal_point.replace('}', '')
                        decimal_point = int(decimal_point)

                        #info = client.futures_exchange_info()
                        maxQty = [globals()['buycoin_buy_{}'.format(n)]]
                        maxQty = {si['symbol']:si['filters'] for si in info['symbols'] if si['symbol'] in maxQty}
                        maxQty = maxQty[globals()['buycoin_buy_{}'.format(n)]]
                        maxQty = maxQty[2]#일단 정보 배열에서 2번째 마켓 최대수량을 가져오지만 만약 해당 배열이 변경될경우 오류가 날수 있음
                        maxQty = float(maxQty['maxQty'])
                        number_of_divisions = 1
                        divisions_purchasing_volume = globals()['old_plus_buy_{}'.format(n)]

                        print('try sell(long) :', globals()['buycoin_buy_{}'.format(n)])
                        if maxQty > divisions_purchasing_volume :
                            #판매
                            client.futures_create_order(
                                symbol=globals()['buycoin_buy_{}'.format(n)], side='SELL',
                                positionSide = 'LONG', type='MARKET', quantity=round(globals()['old_plus_buy_{}'.format(n)],decimal_point)
                            )
                        else :
                            print('#########DIVISION SELL TRY###########')
                            while True:
                                #최대수량보다 구매수량이 클 경우 나눌 횟수 계산
                                if maxQty < divisions_purchasing_volume :
                                    number_of_divisions = number_of_divisions*2
                                    divisions_purchasing_volume = globals()['old_plus_buy_{}'.format(n)]/number_of_divisions
                                else :
                                    for j in range(0, number_of_divisions):
                                        #판매
                                        client.futures_create_order(
                                            symbol=globals()['buycoin_buy_{}'.format(n)], side='SELL',
                                            positionSide = 'LONG', type='MARKET', quantity=round(divisions_purchasing_volume,decimal_point)
                                        )
                                        time.sleep(1)
                                    break

                        print('time :', now)
                        print('success sell coin(long) :', globals()['buycoin_buy_{}'.format(n)])
                        print('----------------------------------------------------')
                        globals()['count_buy_{}'.format(n)] = 'true'
                        time.sleep(1)    

                    now_rsi = float(rsi(globals()['buycoin_buy_{}'.format(n)]).iloc[-1])
                    old_rsi = float(rsi(globals()['buycoin_buy_{}'.format(n)]).iloc[-2])
                    old_old_rsi = float(rsi(globals()['buycoin_buy_{}'.format(n)]).iloc[-3])
                        
############물타기(롱)############
                    #if (30 > old_old_rsi) and (30 < old_rsi) and (30 < now_rsi) and (now > globals()['buytime_buy_{}'.format(n)]) and ((float(globals()['last_current_price_buy_{}'.format(n)]) * float(globals()['increase_water_buy_{}'.format(n)])) > globals()['current_price_buy_{}'.format(n)]):
                    if False:
                        #선물잔고조회
                        balance = binance.fetch_balance(params={"type": "future"})
                        
                        if (globals()['last_buy_money_{}'.format(n)]*2 < balance['USDT']['free']) :
                            #구매가 이전보다 2배 증가
                            globals()['last_buy_money_{}'.format(n)] = globals()['last_buy_money_{}'.format(n)]*2

                            #레버리지 설정
                            client.futures_change_leverage(symbol = globals()['buycoin_buy_{}'.format(n)], leverage = all_leverage)

                            #quantity 자리수 설정
                            client = r_Client(api_key=api_key, api_secret=secret)
                            info = client.futures_exchange_info()
                            requestedFutures = [globals()['buycoin_buy_{}'.format(n)]]
                            decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                            decimal_point = decimal_point.replace('{', '')
                            decimal_point = decimal_point.replace('}', '')
                            decimal_point = int(decimal_point)

                            #info = client.futures_exchange_info()
                            maxQty = [globals()['buycoin_buy_{}'.format(n)]]
                            maxQty = {si['symbol']:si['filters'] for si in info['symbols'] if si['symbol'] in maxQty}
                            maxQty = maxQty[globals()['buycoin_buy_{}'.format(n)]]
                            maxQty = maxQty[2]#일단 정보 배열에서 2번째 마켓 최대수량을 가져오지만 만약 해당 배열이 변경될경우 오류가 날수 있음
                            maxQty = float(maxQty['maxQty'])
                            
                            print('try water buy(long) :', globals()['buycoin_buy_{}'.format(n)])

                            if maxQty > (globals()['buy_money_buy_{}'.format(n)]*2) :
                                #구매
                                client.futures_create_order(
                                    symbol=globals()['buycoin_buy_{}'.format(n)], side='BUY',
                                    positionSide = 'LONG', type='MARKET', quantity=round(globals()['buy_money_buy_{}'.format(n)]*2,decimal_point)
                                )
                            else :
                                divisions_purchasing_volume_buy = globals()['buy_money_buy_{}'.format(n)]*2
                                number_of_divisions_buy = 1
                                while True:
                                    #최대수량보다 구매수량이 클 경우 나눌 횟수 계산
                                    if maxQty < divisions_purchasing_volume_buy :
                                        number_of_divisions_buy = number_of_divisions_buy*2
                                        divisions_purchasing_volume_buy = (globals()['buy_money_buy_{}'.format(n)]*2)/number_of_divisions_buy
                                    else :
                                        for j in range(0, number_of_divisions_buy):
                                            #구매
                                            client.futures_create_order(
                                                symbol=globals()['buycoin_buy_{}'.format(n)], side='BUY',
                                                positionSide = 'LONG', type='MARKET', quantity=round(divisions_purchasing_volume_buy,decimal_point)
                                            )
                                            time.sleep(1)
                                        break

                            #구매시간 갱신
                            globals()['buytime_buy_{}'.format(n)] = dt.datetime.now() + dt.timedelta(minutes=delay_time)
                            #물타기가격 갱신(2배)
                            globals()['old_buy_money_buy_{}'.format(n)] = globals()['buy_money_buy_{}'.format(n)]
                            globals()['buy_money_buy_{}'.format(n)] = float(globals()['buy_money_buy_{}'.format(n)])*2
                            globals()['current_price_buy_{}'.format(n)] = client.futures_symbol_ticker(symbol=globals()['buycoin_buy_{}'.format(n)])
                            globals()['current_price_buy_{}'.format(n)] = float(globals()['current_price_buy_{}'.format(n)]['price'])
                            globals()['last_current_price_buy_{}'.format(n)] = globals()['current_price_buy_{}'.format(n)]

                            #총 매수량
                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']
                            for position in positions:
                                if (position["symbol"] == globals()['buycoin_buy_{}'.format(n)]) and (position["positionSide"] == "LONG"):
                                    entry = position['entryPrice']
                                    positionAmt = position['positionAmt']
                                    print('entry',entry)
                                    print('positionAmt',positionAmt)
                                    break

                            globals()['water_buy_price_buy_{}'.format(n)] = float(entry)
                            globals()['old_plus_buy_{}'.format(n)] = float(positionAmt)
                            #물타기 점진적 증가 값
                            globals()['increase_water_buy_{}'.format(n)] = float(globals()['increase_water_buy_{}'.format(n)])-0.05
                            print('time :', now)
                            print('success water coin(long) :', globals()['buycoin_buy_{}'.format(n)])
                            print('old_old_rsi(long)', old_old_rsi)
                            print('old_rsi(long)', old_rsi)
                            print('----------------------------------------------------')
                            time.sleep(1)    
                            
                
                if (globals()['count_sell_{}'.format(n)] == 'false'):
                    #코인 현재가(숏)
                    client = r_Client(api_key=api_key, api_secret=secret)
                    globals()['current_price_sell_{}'.format(n)] = client.futures_symbol_ticker(symbol=globals()['buycoin_sell_{}'.format(n)])
                    globals()['current_price_sell_{}'.format(n)] = float(globals()['current_price_sell_{}'.format(n)]['price'])
                    
####################1퍼 익절(숏)####################
                    if ((float(globals()['water_buy_price_sell_{}'.format(n)]) * 0.99) > globals()['current_price_sell_{}'.format(n)]) :

                        #quantity 자리수 설정
                        client = r_Client(api_key=api_key, api_secret=secret)
                        info = client.futures_exchange_info()
                        requestedFutures = [globals()['buycoin_sell_{}'.format(n)]]
                        decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                        decimal_point = decimal_point.replace('{', '')
                        decimal_point = decimal_point.replace('}', '')
                        decimal_point = int(decimal_point)

                        #info = client.futures_exchange_info()
                        maxQty = [globals()['buycoin_sell_{}'.format(n)]]
                        maxQty = {si['symbol']:si['filters'] for si in info['symbols'] if si['symbol'] in maxQty}
                        maxQty = maxQty[globals()['buycoin_sell_{}'.format(n)]]
                        maxQty = maxQty[2]#일단 정보 배열에서 2번째 마켓 최대수량을 가져오지만 만약 해당 배열이 변경될경우 오류가 날수 있음
                        maxQty = float(maxQty['maxQty'])
                        number_of_divisions = 1
                        divisions_purchasing_volume = globals()['old_plus_sell_{}'.format(n)]

                        print('try sell(short) :', globals()['buycoin_sell_{}'.format(n)])
                        if maxQty > divisions_purchasing_volume :
                            #판매
                            client.futures_create_order(
                                symbol=globals()['buycoin_sell_{}'.format(n)], side='BUY',
                                positionSide = 'SHORT', type='MARKET', quantity=round(globals()['old_plus_sell_{}'.format(n)],decimal_point)
                            )
                        else :
                            print('#########DIVISION SELL TRY###########')
                            while True:
                                #최대수량보다 구매수량이 클 경우 나눌 횟수 계산
                                if maxQty < divisions_purchasing_volume :
                                    number_of_divisions = number_of_divisions*2
                                    divisions_purchasing_volume = globals()['old_plus_sell_{}'.format(n)]/number_of_divisions
                                    print(number_of_divisions)
                                    print(divisions_purchasing_volume)
                                else :
                                    for j in range(0, number_of_divisions):
                                        #판매
                                        client.futures_create_order(
                                            symbol=globals()['buycoin_sell_{}'.format(n)], side='BUY',
                                            positionSide = 'SHORT', type='MARKET', quantity=round(divisions_purchasing_volume,decimal_point)
                                        )
                                        time.sleep(1)
                                    break

                        print('time :', now)
                        print('success sell coin(short) :', globals()['buycoin_sell_{}'.format(n)])
                        print('----------------------------------------------------')
                        globals()['count_sell_{}'.format(n)] = 'true'  
                        time.sleep(1)    

                    now_rsi = float(rsi(globals()['buycoin_sell_{}'.format(n)]).iloc[-1])
                    old_rsi = float(rsi(globals()['buycoin_sell_{}'.format(n)]).iloc[-2])
                    old_old_rsi = float(rsi(globals()['buycoin_sell_{}'.format(n)]).iloc[-3])

############물타기(숏)############
                    #if (70 < old_old_rsi) and (70 > old_rsi) and (70 > now_rsi) and (now > globals()['buytime_sell_{}'.format(n)]) and ((float(globals()['last_current_price_sell_{}'.format(n)]) * float(globals()['increase_water_sell_{}'.format(n)])) < globals()['current_price_sell_{}'.format(n)]):
                    if False:
                        #선물잔고조회
                        balance = binance.fetch_balance(params={"type": "future"})
                        
                        if (globals()['last_sell_money_{}'.format(n)]*2 < balance['USDT']['free']) :
                            globals()['last_sell_money_{}'.format(n)] = globals()['last_sell_money_{}'.format(n)]*2
                            #레버리지 설정
                            client.futures_change_leverage(symbol = globals()['buycoin_sell_{}'.format(n)], leverage = all_leverage)

                            #quantity 자리수 설정
                            client = r_Client(api_key=api_key, api_secret=secret)
                            info = client.futures_exchange_info()
                            requestedFutures = [globals()['buycoin_sell_{}'.format(n)]]
                            decimal_point = str({si['quantityPrecision'] for si in info['symbols'] if si['symbol'] in requestedFutures})
                            decimal_point = decimal_point.replace('{', '')
                            decimal_point = decimal_point.replace('}', '')
                            decimal_point = int(decimal_point)

                            #info = client.futures_exchange_info()
                            maxQty = [globals()['buycoin_sell_{}'.format(n)]]
                            maxQty = {si['symbol']:si['filters'] for si in info['symbols'] if si['symbol'] in maxQty}
                            maxQty = maxQty[globals()['buycoin_sell_{}'.format(n)]]
                            maxQty = maxQty[2]#일단 정보 배열에서 2번째 마켓 최대수량을 가져오지만 만약 해당 배열이 변경될경우 오류가 날수 있음
                            maxQty = float(maxQty['maxQty'])

                            print('try water buy(short) :', globals()['buycoin_sell_{}'.format(n)])

                            if maxQty > (globals()['buy_money_sell_{}'.format(n)]*2) :
                                #구매
                                client.futures_create_order(
                                    symbol=globals()['buycoin_sell_{}'.format(n)], side='SELL',
                                    positionSide = 'SHORT', type='MARKET', quantity=round(globals()['buy_money_sell_{}'.format(n)]*2,decimal_point)
                                )
                            else :
                                divisions_purchasing_volume_sell = globals()['buy_money_sell_{}'.format(n)]*2
                                number_of_divisions_sell = 1
                                while True:
                                    #최대수량보다 구매수량이 클 경우 나눌 횟수 계산
                                    if maxQty < divisions_purchasing_volume_sell :
                                        number_of_divisions_sell = number_of_divisions_sell*2
                                        divisions_purchasing_volume_sell = (globals()['buy_money_sell_{}'.format(n)]*2)/number_of_divisions_sell
                                    else :
                                        for j in range(0, number_of_divisions_sell):
                                            #구매
                                            client.futures_create_order(
                                                symbol=globals()['buycoin_sell_{}'.format(n)], side='SELL',
                                                positionSide = 'SHORT', type='MARKET', quantity=round(divisions_purchasing_volume_sell,decimal_point)
                                            )
                                            time.sleep(1)
                                        break

                            #구매시간 갱신
                            globals()['buytime_sell_{}'.format(n)] = dt.datetime.now() + dt.timedelta(minutes=delay_time)
                            #물타기가격 갱신(2배)
                            globals()['old_buy_money_sell_{}'.format(n)] = globals()['buy_money_sell_{}'.format(n)]
                            globals()['buy_money_sell_{}'.format(n)] = globals()['buy_money_sell_{}'.format(n)]*2
                            globals()['current_price_sell_{}'.format(n)] = client.futures_symbol_ticker(symbol=globals()['buycoin_sell_{}'.format(n)])
                            globals()['current_price_sell_{}'.format(n)] = float(globals()['current_price_sell_{}'.format(n)]['price'])
                            globals()['last_current_price_sell_{}'.format(n)] = globals()['current_price_sell_{}'.format(n)]

                            #총 매수량
                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']
                            for position in positions:
                                if (position["symbol"] == globals()['buycoin_sell_{}'.format(n)]) and (position["positionSide"] == "SHORT"):
                                    entry = position['entryPrice']
                                    positionAmt = -float(position['positionAmt'])
                                    print('entry',position['entryPrice'])
                                    print('positionAmt',positionAmt)
                                    break
                            
                            globals()['water_buy_price_sell_{}'.format(n)] = float(entry)
                            globals()['old_plus_sell_{}'.format(n)] = positionAmt
                            #물타기 점진적 증가 값
                            globals()['increase_water_sell_{}'.format(n)] = float(globals()['increase_water_sell_{}'.format(n)])+0.05
                            print('time :', now)
                            print('success water coin(short) :', globals()['buycoin_sell_{}'.format(n)])
                            print('old_old_rsi(short)', old_old_rsi)
                            print('old_rsi(short)', old_rsi)
                            print('----------------------------------------------------')
                            time.sleep(1)    
  
                time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(2)
        i = i+1
