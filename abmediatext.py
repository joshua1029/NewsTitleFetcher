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
    
    return abTitle

def getAbImg(pages=1):  # 定義函數並給予默認頁碼為1
    def getImg(imgs):  # 定義內部函數用來處理圖片URL
        img_urls = []  # 初始化一個空的列表用來存放圖片URL
        for img in imgs:  # 遍歷每一個圖片元素
            try:
                if "abmedia" in img["src"]:  # 檢查圖片URL中是否包含"abmedia"
                    img_urls.append(img["src"])  # 如果包含，將其添加到列表中
            except:
                pass  # 如果有錯誤，就跳過
        return img_urls  # 返回整理好的圖片URL列表

    # 這邊開始是用selenium來開啟網頁並獲取內容
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
    driver.get(f"https://abmedia.io/blog/page/{pages}")  # 根據頁碼打開特定頁面
    time.sleep(1)  # 等待1秒確保網頁加載完成
    html = driver.page_source  # 獲取網頁的HTML內容

    soup = bs4.BeautifulSoup(html, "html.parser")  # 使用BeautifulSoup解析HTML
    imgs = soup.find_all("img")  # 找到所有的圖片元素
    
    img_urls = getImg(imgs)  # 使用getImg獲取圖片URL
    driver.quit()  # 關閉瀏覽器
    
    return img_urls  

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