from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
 
 
# # 美食抽象類別
# class Food(ABC):
 
#     def __init__(self, area):
#         self.area = area  # 地區
 
#     @abstractmethod
#     def scrape(self):
#         pass
 
# # 愛食記爬蟲
# class IFoodie(Food):
 
def scrape(self):
    response = requests.get(
        "https://ifoodie.tw/explore/" + self +
        "/list?sortby=rating&opening=true&priceLevel=2")

    soup = BeautifulSoup(response.content, "html.parser")

    # 前五筆餐廳卡片資料
    cards = soup.find_all(
        'div', {'class': 'jsx-558691085 restaurant-item track-impression-ga'}, limit=5)

    content = ""
    for card in cards:

        title = card.find(  # 餐廳名稱
            "a", {"class": "jsx-558691085 title-text"}).getText()

        stars = card.find(  # 餐廳評價
            "div", {"class": "jsx-1207467136 text"}).getText()

        address = card.find(  # 餐廳地址
            "div", {"class": "jsx-558691085 address-row"}).getText()

        content += f"{title} \n{stars}顆星 \n{address} \n\n"

    return content

#print(scrape("台中市"))