
# print("心理測驗：今天你想吃什麼？")
# print("注意：每題只能選擇一個答案，應為你第一直覺的答案") 
# print("開始心理測驗：")
 
#由于计算总值
food_price=0
food_taste=0

Questions = [
    "1、你想送一束花給你的摯友，\n哪一束花比較合適？",
    "2、可以向阿拉丁神燈許一個願望，\n你想要？",
    "3、你疫情結束後，你最想要？",
    "4、想像你現在就有一張\n可以飛去世界各地\n的機票，你會想去哪？",
    "5、在裝修新房子的時候，\n你會在哪一部分花最多錢？",
    "6、假如有天早上醒來發現自己\n被外星人抓走，你打算怎麼做？",
    "7、在路上看到一個拾荒老人，\n推著裝滿一車子東西的推車經過，\n突然從車上掉下一包\n用髒抹布包著的不明包裹，\n你覺得裡面可能會是？",
    "8、你的房間有一扇窗戶，\n可以眺望外面的風景。\n如果現在要加上窗簾，\n你會選哪一個款式？"
]

Options = [
    "1.美麗動人的玫瑰,2.淡雅怡人的桂花,3.純白潔淨的茉莉,4.可愛俏皮的雞蛋花",
    "1.無盡的財富,2.真摯的靈魂伴侶,3.至高無上的權力跟地位,4.順心滿意的生活",
    "1.去健身房大汗淋漓,2.進電影院看一場精彩的電影,3.到酒吧小酌怡情,4.到KTV放聲高歌一場",
    "1.去峇里島浮淺,2.去冰島看極光,3.去日本賞櫻花,4.去威尼斯欣賞古蹟",
    "1.客廳的沙發、擺設,2.臥室的床,3.浴室,4.廚房",
    "1.想辦法逃走,2.裝死,3.求他們放自己走,4.與外星人拚死搏鬥",
    "1.礦泉水,2.便當盒,3.香菸,4.裝錢的盒子",
    "1.素色,2.方格線條,3.花朵款式,4.白紗窗簾"
]

Score = [
    ["taste", 3, 2, 4, 1],
    ["price", 4, 1, 3, 2],
    ["taste", 4, 1, 2, 3],
    ["price", 2, 4, 1, 3],
    ["price", 1, 2, 3, 4],
    ["price", 3, 4, 1, 2],
    ["taste", 3, 2, 4, 1],
    ["taste", 2, 3, 4, 1]
]

Result = [
    "牛肉麵",
    "牛排",
    "火鍋",
    "義大利麵",
    "拉麵",
    "咖哩",
    "健康餐",
    "水餃"
]


def calculate_result(user_result):
    food_taste, food_price = 0,0 
    for status in range(1, 8):
        question = status - 1
        ans = user_result[status]
        if Score[question][0] == 'taste':
            food_taste += Score[question][ans]
        elif Score[question][0] == 'price':
            food_price += Score[question][ans]
    
    if food_price >= 13:
        if food_taste >= 13:
            return food_price, food_taste, 1
        elif 9 <= food_taste < 13:
            return food_price, food_taste, 4
        else:
            return food_price, food_taste, 2
    elif 9 <= food_price < 13:
        if food_taste >= 13:
            return food_price, food_taste, 5
        elif 9 <= food_taste < 13:
            return food_price, food_taste, 0
        else:
            return food_price, food_taste, 3
    else:
        if food_taste >= 10:
            return food_price, food_taste, 6
        else:
            return food_price, food_taste, 7
