# 鏈新聞爬蟲 爬新聞標題

import urllib.request as req # 用於處理URL請求
import bs4 # 用於解析HTML
import os
import time # 停頓用的
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager # 國外鬼神做的webdriver管理器 比原本的方法好用多了
from selenium.webdriver.common.by import By # find_element的By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def getAbTitle(pages, keyword):
    def getTitle(url, count, keyword, seen):
        # 這裡是要假裝程式是真人對瀏覽器發送請求 
        request = req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        })
        
        # 這裡是在打開網頁和獲取內容  
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8") # decode("utf-8")避免出現亂碼
        
        # 使用BeautifulSoup來解析網頁的內容
        root = bs4.BeautifulSoup(data, "html.parser")
        titles = root.find_all("h3", class_="title")
        
        abTitles = []
        
        for title in titles:
            if title.a != None:
                title_text = title.a.string
                # 這裡是為了讓它不要輸出同樣的標題用和篩選關鍵字用的
                if title_text not in seen and keyword in title_text:
                    abTitles.append(title_text)
                    seen.add(title_text) # 把已經出現過的標題放進seen的集合裡
                           
        # 一頁結束 準備下一頁的連結            
        count += 1 
        nextpage = root.find("a", string=f"{count}")
        
        # 確認還有下一頁後回傳
        if nextpage is not None: 
            return nextpage["href"], abTitles
        else:
            return None, abTitles

    #我想爬的網站
    pageurl = "https://abmedia.io/blog"  

    count = 1
    seen = set() # 為了不讓輸出同樣內容而設置的集合
    abTitle = [] # 放標題用的

    while count <= pages and pageurl is not None:
        pageurl, titles = getTitle(pageurl, count, keyword, seen)
        abTitle.extend(titles)
        count += 1
    
    print(abTitle)
    #return abTitle

def getAbImg():
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
    driver.quit()

# 測試用的
def main():
    print("選擇功能：")
    print("1. 爬取圖片")
    print("2. 爬取新聞標題")
    print("3. 同時爬取圖片和新聞標題")
    choice = int(input("請輸入選擇（1/2/3）："))

    if choice == 1:
        getAbImg()
    elif choice == 2:
        pages = int(input("請輸入想要幾頁 : "))
        keyword = str(input("請輸入想要的關鍵字 : "))
        getAbTitle(pages, keyword)
    elif choice == 3:
        getAbImg()
        pages = int(input("請輸入想要幾頁 : "))
        keyword = str(input("請輸入想要的關鍵字 : "))
        getAbTitle(pages, keyword)
    else:
        print("無效的選擇。")


main()