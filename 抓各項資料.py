# 股票資料類別
class stinfo:
    # 建構式
    def __init__(self, ID):
        self.id = ID  # 股票代號
    # 現值方法(nowvalue Method)
    def now(self):
        #引用yahoo_fin套件並縮寫為si
        import yahoo_fin.stock_info as si
        #抓現價
        now = si.get_live_price(self.id)
        #回傳現價
        return now
    # 今日及時k線(nowvalue K LINE Method)
    def today(self):
        #引用yfinance套件並縮寫為yf
        import yfinance as yf
        #引用matplot套件並縮寫為plt
        import matplotlib.pyplot as plt
        #引用mpl_finance套件並縮寫為mpf
        import mpl_finance as mpf
        # 下載今日數據
        # 時間範圍1天
        # 時間頻率5分鐘
        data = yf.download(self.id,
                           period='1d',
                           interval='5m')
        #因為抓下來的資料index本身就含有時間屬性
        #所以不用特別更動
        #但因為原本的時間屬性包含了日期
        #所以我將他強制留下時分秒三者資訊
        data.index = data.index.format(
            formatter=lambda x: x.strftime('%H-%M-%S'))
        # 空白畫布
        fig = plt.figure(figsize=(24, 15))
        # 空白畫布上半部大小
        ax0 = fig.add_axes([0.08, 0.3, 0.9, 0.6])
        # 空白畫布下半部大小
        ax1 = fig.add_axes([0.08, 0.05, 0.9, 0.2])
        # 設定畫布上半部X軸的數據區間
        ax0.set_xticks(range(0, len(data.index), 10))
        # 設定畫布上半部X軸上的資訊
        ax0.set_xticklabels(data.index[::10])
        #畫K線的上下引線
        mpf.candlestick2_ochl(ax0, data['Open'], data['Close'], data['High'],
                              data['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
        #畫K線的身體
        mpf.volume_overlay(ax1, data['Open'], data['Close'], data['Volume'],
                           colorup='r', colordown='g', width=0.5, alpha=0.8)
        #設定畫布下半部X軸的數據區間
        ax1.set_xticks(range(0, len(data.index), 10))
        #設定畫布下半部X軸上的資訊
        ax1.set_xticklabels(data.index[::10])
        # 回傳數據及圖片
        return data, plt
    # 某個月的日本益比
    def per(self, date):
        # 引用pandas套件並縮寫為pd
        import pandas as pd
        # 引用urllib套件並縮寫為req
        import urllib.request as req
        # 引用bs4套件並縮寫為bs
        from bs4 import BeautifulSoup as bs
        # 設定爬蟲網址
        url = f"https://www.twse.com.tw/exchangeReport/BWIBBU?response=html&date={date}&stockNo={self.id[:4]}"
        # 爬蟲
        # 要記得設定headers
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        })
        # 利用utf-8解讀爬蟲到的資料
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        # 利用bs中的 lxml解讀數據
        bsobj_1 = bs(data, "lxml")
        # 從前面抓到的 html 在 bsobj_1 中找所有 table 標籤
        tables = bsobj_1.find_all('table')
        # 在從 table 中再去尋找 tr 標籤 會找到很多陣列
        trs = tables[0].find_all('tr')
        # 設置一些空變量以便後續使用
        trNum = 0
        tdNum = 0
        result = []
        # 利用迴圈將所有 tr 陣列中每個 
        # td 標籤的資料 抓出來
        for i in range(len(trs)):
            tds = trs[i].find_all('td')
            # 跳過沒有內容的 tr
            if len(tds) < 5:  
                continue
            trNum += 1
            tdNum = 0
            # 設置空變量以便後續使用
            tempList = []
            for j in tds:
                # 去掉文字中的 \xa0 空白字元
                if j.text == '\xa0':
                    continue
                # 將每個陣列中的資料切割
                tempText = "".join(j.text.split()) 
                # 再放進前面的空白陣列
                tempList.append(tempText)
                tdNum += 1
            # 將前面得到的陣列並起來
            result.append(tempList)
        # 將原本的雙重陣列轉成 dataframe 欄位名稱是第一個陣列
        result = pd.DataFrame(result[1:], columns=result[0])
        #回傳最後得到的資料
        return result
    # 盤後資料
    def ahd(self):
        # 引用 yahoo_fin 套件並縮寫為 si
        import yahoo_fin.stock_info as si
        # get_data 可以抓到盤後的所有資料
        data = si.get_data(self.id)
        # 回傳 盤後資料
        return data
    # 找大股東資料
    def findbig(self):
        # 引用pandas套件並縮寫為pd
        import pandas as pd
        # 引用urllib套件並縮寫為req
        import urllib.request as req
        # 引用bs4套件並縮寫為bs
        from bs4 import BeautifulSoup as bs
        # 設定爬蟲網址
        url = "https://norway.twsthr.info/StockHolders.aspx?stock=2330"
        # 爬蟲
        # 要記得設定headers
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        })
        # 利用utf-8解讀爬蟲到的資料
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        # 利用bs中的 lxml解讀數據
        bsobj_1 = bs(data, "lxml")
        # 從前面抓到的 html 在 bsobj_1 中找所有 table 標籤
        # 找出回傳之分散表
        tables = bsobj_1.find_all('table', id="Details")
        # 在從 table 中再去尋找 tr 標籤 會找到很多陣列
        trs = tables[0].find_all('tr')
        # 設置一些空變量以便後續使用
        trNum = 0
        tdNum = 0
        result = []
        # 利用迴圈將所有 tr 陣列中每個 
        # td 標籤的資料 抓出來
        for i in range(len(trs)):
            tds = trs[i].find_all('td')
            if len(tds) < 5:  # 跳過沒有內容的 tr
                continue
            trNum += 1
            tdNum = 0
            # 設置空變量以便後續使用
            tempList = []
            for j in tds:
                # 去掉文字中的 \xa0 空白字元
                if j.text == '\xa0':
                    continue
                
                # 將每個陣列中的資料切割
                tempText = "".join(j.text.split()) 
                # 再放進前面的空白陣列
                tempList.append(tempText)
                tdNum += 1
            # 將前面得到的陣列並起來
            result.append(tempList)
        # 將原本的雙重陣列轉成 dataframe 欄位名稱是第一個陣列
        result = pd.DataFrame(result[1:],columns=result[0])
        #回傳最後得到的資料
        return result
mazda = stinfo("2330.TW")
k = mazda.now()
today, l = mazda.today()
k0=mazda.per('20211101')
# k1=mazda.ahd()
# k2 = mazda.findbig()
print(k0)
