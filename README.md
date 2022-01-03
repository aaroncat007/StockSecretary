# StockSecretary

## Contents

Bot is [t.me/StockSecretary_bot](https://t.me/StockSecretary_bot) .   
HTTP API Token is Written in ``main.py`` API_TOKEN variable
## Getting started

This API is tested with Python 3.6-3.10 and Pypy 3.
There are two ways to install the library:

* Installation using pip (a Python package manager)*:

```
$ pip install -r requirements.txt 
```

* Run Start:
```
$ python main.py
```

## Structure

```
`-- src  
    |-- Models                     # 資料層
    |  |-- dbModel.py               # 基礎模型
    |  |-- CSVModel.py              # CSV資料庫
    |  |-- UserModel.py             # 用戶模型
    |-- Repository                 # 倉儲層
    |  |-- BaseRepository.py        # 基礎倉儲
    |  |-- SQLiteRepository.py      # SQLite 資料倉儲
    |-- Services                   # 服務層
    |  |-- MessageHandler.py        # 服務基底
    |  |-- HelpHandler.py           # 幫助我服務
    |  |-- SerachStockHandler.py    # 查詢股票服務
    |  |-- TWStockHandler.py        # 大盤資訊服務
    |-- main.py                    # 主程序
```
