from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# 1. 首頁 (整合天氣預報與交通推薦)
@app.route('/')
def index():
    # 模擬天氣數據 (適合期末報告穩定展示，免去 API 失效風險)
    weather_data = {
        "city": "台北市",
        "temp": "28°C",
        "condition": "多雲偶陣雨",
        "humidity": "75%"
    }
    
    # 交通推薦邏輯
    traffic_tips = [
        "捷運：台北車站轉乘板南線、淡水信義線最便利。",
        "公車：下雨天班次可能稍有延誤，建議提早出門。",
        "共享機車：雨天路滑，騎乘 WeMo / GoShare 請注意安全。"
    ]
    
    return render_template('index.html', weather=weather_data, tips=traffic_tips)

# 2. 股票查詢頁面
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    stock_info = None
    error_msg = None
    ticker = "2330.TW" # 預設顯示台積電
    
    if request.method == 'POST':
        user_input = request.form.get('ticker_input', '').strip()
        if user_input:
            ticker = user_input

    try:
        # 使用 yfinance 抓取股票資料
        stock_data = yf.Ticker(ticker)
        info = stock_data.info
        
        # 處理台股與美股的名稱顯示
        stock_info = {
            "name": info.get('longName', ticker),
            "symbol": ticker,
            "price": info.get('currentPrice') or info.get('regularMarketPrice') or "無資料",
            "currency": info.get('currency', 'USD'),
            "summary": info.get('longBusinessSummary', '暫無公司簡介。')
        }
    except Exception as e:
        error_msg = f"找不到股票代號 '{ticker}' 或資料擷取失敗，台股請記得加 .TW (例如: 2330.TW)"

    return render_template('stock.html', stock=stock_info, error=error_msg)

# 3. 台北美食介紹頁面
@app.route('/food')
def food():
    # 台北美食靜態資料庫
    taipei_foods = [
        {
            "name": "鼎泰豐 (信義店)",
            "area": "大安區",
            "type": "中式點心",
            "desc": "享譽國際的小籠包，皮薄汁多，黃金18摺的工藝絕對是台北代表美食。",
            "recommend": "小籠包、排骨蛋炒飯"
        },
        {
            "name": "大橋頭老牌筒仔米糕",
            "area": "大同區",
            "type": "在地小吃",
            "desc": "延三夜市的經典老店，米糕粒粒分明，肥肉與瘦肉可依個人喜好選擇。",
            "recommend": "筒仔米糕、豬肝湯"
        },
        {
            "name": "詹記麻辣火鍋",
            "area": "敦南店",
            "type": "火鍋",
            "desc": "台北超難訂位的麻辣鍋之一，鴨血滑嫩如布丁，豆腐非常入味。",
            "recommend": "滑嫩鴨血、台灣牛胸肉"
        }
    ]
    return render_template('food.html', foods=taipei_foods)

if __name__ == '__main__':
    # 確保在本機測試與 Render 部署時都能正常運行
    app.run(host='0.0.0.0', port=5000, debug=True)
