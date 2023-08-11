# 鏈新聞爬蟲 爬新聞圖片

import os
import time # 停頓用的
import bs4 # 用於解析HTML
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager # 國外鬼神做的webdriver管理器 比原本的方法好用多了
from selenium.webdriver.common.by import By # find_element的By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def getImg(imgs):
    for img in imgs:
        try:
            url = img["src"]
            name = img["alt"]
            os.makedirs("abmediapic", exist_ok=True)
            if len(name) > 5: # 真的找不到其他區分方法 只能用幾個字去判斷了
                resp = requests.get(url)
                img = resp.content
                with open(f"abmediapic/{name}.png", "wb") as file:
                    file.write(img)
        except:
            pass

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install())) 

driver.get("https://abmedia.io/blog")
time.sleep(1)
html = driver.page_source

soup = bs4.BeautifulSoup(html, "html.parser")
imgs = soup.find_all("img")

getImg(imgs)