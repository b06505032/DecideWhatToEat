import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
import webbrowser
import urllib.parse
import lxml

def nearby_location(_keyword, _location):
    location = _location
    # latitude_longitude = 25.017532,121.539727  # 臺大經緯度25.017532,121.539727
    keyword = _keyword  # 搜尋關鍵字，ex:中式餐廳
    APIkey = "GOOGLE_PLACE_API_KEY"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}".format(location) 
    url = url + "&radius=800" + "&language=zh-TW" + "&type=restaurant" + "&keyword=" + str(keyword) + "&key=" + APIkey
    print(url)
    # "&opennow=True"
    gmap = requests.get(url)  # 取得上列網址內容
    gsoup = BeautifulSoup(gmap.text, 'lxml')  # 用beautifulsoup進行解析
    g_info = json.loads(gsoup.text)  # 因原始資料為格式為JSON，所以把JSON格式轉為Python的資料
    consequence = g_info["results"]
    # print("搜尋到的資料總數: ", len(consequence))
    restaurant_name = []
    restaurant_rating = []
    for data in consequence:
        restaurant_name.append(data["name"])
        restaurant_rating.append(data['rating'])
    best_four = []
    highest_restaurant = 0
    
    if len(restaurant_rating) >= 4:
        number = 4
    else:
        number = len(restaurant_rating)
    
    for i in range(number):
        highest_restaurant = restaurant_name[restaurant_rating.index(max(restaurant_rating))]
        best_four.append(highest_restaurant)
        restaurant_rating.pop(restaurant_name.index(highest_restaurant))
        restaurant_name.pop(restaurant_name.index(highest_restaurant))
        # print(restaurant_name.index(highest_restaurant))
    print(best_four)
    return best_four
