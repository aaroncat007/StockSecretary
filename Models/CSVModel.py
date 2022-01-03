#!/usr/bin/python
# -*- coding:utf-8 -*-

from Models.dbModel import dbModel

# CSV 資料庫
class CSVModel(dbModel):

    def __init__(self):
        super().__init__()

    def initTable(self):
        return NotImplemented

    #取得大盤資訊
    def getTWStock(self):
        import yahoo_fin.stock_info as si
        import yfinance as yf
        id='^TWII'
        toclos=float(yf.download(id,
                    period='1d',
                    interval='5m').iloc[-1:]['Close'])
        yes=si.get_data(id).iloc[-1:]
        yeclos=float(yes['close'])
        yesop=float(yes['open']) 
        yeshg=float(yes['high']) 
        yeslo=float(yes['low']) 
        yesvalue=int(yes['volume']) 
        print('大盤情形')
        if toclos>yeclos:
            print('現價',round(toclos,2),f' ▲{toclos-yeclos} ',f'{round((toclos/yeclos-1)*100,2)} %')
            print(f'昨日開盤    {round(yesop,2)}')
            print(f'昨日收盤    {round(yeclos,2)}')
            print(f'昨日最高    {round(yeshg,2)}')
            print(f'昨日最低    {round(yeslo,2)}')
            print(f'昨日成交量    {yesvalue} 張')

        elif toclos==yeclos:
            print('現價',round(toclos,2),f' ●{toclos-yeclos} ',f'{round((toclos/yeclos-1)*100,2)} %')
            print(f'昨日開盤    {round(yesop,2)}')
            print(f'昨日收盤    {round(yeclos,2)}')
            print(f'昨日最高    {round(yeshg,2)}')
            print(f'昨日最低    {round(yeslo,2)}')
            print(f'昨日成交量    {yesvalue} 張')

        else:
            print(toclos,f' ▼{yeclos-toclos} ',f'{round((yeclos/toclos-1)*100,2)} %')
            print(f'昨日開盤    {round(yesop,2)}')
            print(f'昨日收盤    {round(yeclos,2)}')
            print(f'昨日最高    {round(yeshg,2)}')
            print(f'昨日最低    {round(yeslo,2)}')
            print(f'昨日成交量  {yesvalue} 張')




        return """\
加權指數 0000
17812.59 ▲26.85 0.15%
開盤 17744.54
昨收 17785.74
最高 17822.74
最低 17718.27
成交量(億) 3,459.2
預估量(億) 3,459\
"""