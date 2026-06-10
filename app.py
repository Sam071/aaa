from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 1. 交通系統資料 (模擬台北捷運路線)
mrt_data = {
    "板南線": ["頂埔", "板橋", "西門", "台北車站", "忠孝復興", "市政府", "南港展覽館"],
    "淡水信義線": ["象山", "台北101/世貿", "大安", "台北車站", "中山", "士林", "淡水"],
    "松山新店線": ["新店", "公館", "中正紀念堂", "西門", "中山", "南京復興", "松山"]
}

# 2. 台北美食資料庫
food_data = [
    {"name": "阿宗麵線", "area": "萬華區 (西門町)", "category": "平民小吃", "desc": "鼎鼎大名的柴魚湯頭麵線，站著吃也是一種特色。"},
    {"name": "鼎泰豐", "area": "大安區 (信義店)", "category": "餐廳/小籠包", "desc": "黃金18摺小籠包，服務與餐點品質都是國際級水準。"},
    {"name": "林東芳牛肉麵", "area": "中山區", "category": "在地美食", "desc": "濃郁的中藥牛肉湯頭，加上特製辣牛油堪稱一絕。"},
    {"name": "阜杭豆漿", "area": "中正區", "category": "早餐點心", "desc": "天天大排長龍的傳統早餐，厚餅夾蛋與鹹豆漿是必點招牌。"},
    {"name": "師大夜市 燈籠滷味", "area": "大安區", "category": "夜市小吃", "desc": "加熱滷味的經典代表，獨門中藥醬汁讓人一口接一口。"},
    {"name": "九份賴阿婆芋圓", "area": "瑞芳區", "category": "傳統甜點", "desc": "口感極具彈性的手工芋圓，冷熱皆宜的老字號美味。"}
]

# 首頁路由
@app.route('/')
def index():
    return render_template('index.html')

# 交通系統路由
@app.route('/transport')
def transport():
    return render_template('transport.html', mrt_lines=mrt_data)

# 交通系統的 API (提供給前端網頁動態刷新倒數時間)
@app.route('/api/mrt/<line>')
def get_mrt_status(line):
    stations = mrt_data.get(line, [])
    status_list = []
    for s in stations:
        status_list.append({
            "station": s,
            "next_train": f"{random.randint(1, 6)} 分鐘",
            "crowd": random.choice(["舒適", "普通", "擁擠"])
        })
    return jsonify(status_list)

# 天氣預報路由
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    selected_district = request.form.get('district', '中正區')
    
    # 動態模擬各區氣象數據
    weather_status = ["晴時多雲", "陰天", "短暫陣雨", "午後雷陣雨", "晴朗舒適"]
    temp = random.randint(22, 34)
    humidity = random.randint(60, 85)
    
    current_weather = {
        "district": selected_district,
        "status": random.choice(weather_status),
        "temp": temp,
        "humidity": humidity,
        "suggestion": "紫外線較強，出門記得做好防曬並多補充水分！" if temp > 30 else "目前氣候舒適，非常適合安排一趟美食之旅！"
    }
    return render_template('weather.html', weather=current_weather)

# 美食介紹路由 (包含搜尋功能)
@app.route('/food')
def food():
    search_query = request.args.get('search', '')
    if search_query:
        # 關鍵字比對名稱、區域或分類
        filtered_food = [
            f for f in food_data 
            if search_query.lower() in f['name'].lower() 
            or search_query.lower() in f['area'].lower() 
            or search_query.lower() in f['category'].lower()
        ]
    else:
        filtered_food = food_data
    return render_template('food.html', foods=filtered_food, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
