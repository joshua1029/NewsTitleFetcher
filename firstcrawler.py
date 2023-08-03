import urllib.request as req #用於處理URL請求
import bs4 #用於解析HTML

def getData(url, count, seen):
    #這裡是要假裝程式是真人對瀏覽器發送請求 
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    })
    
    #這裡是在打開網頁和獲取內容  
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8") #decode("utf-8")避免出現亂碼
    
    #使用BeautifulSoup來解析網頁的內容
    root = bs4.BeautifulSoup(data, "html.parser")
    titles = root.find_all("h3", class_="title")
        
    for title in titles:
        if title.a != None:
            title_text = title.a.string
            #這裡是為了讓它不要輸出同樣的標題用的
            if title_text not in seen:
                with open("chain.txt", mode="a", encoding="utf-8") as file:
                    file.write(title_text + "\n")
                seen.add(title_text) #把已經出現過的標題放進seen的集合裡
    
    #一頁結束 準備下一頁的連結            
    count += 1 
    nextpage = root.find("a", string=f"{count}")
    return nextpage["href"]

#我想爬的網站
pageurl = "https://abmedia.io/blog"    

count = 1
seen = set() #為了不讓輸出同樣內容而設置的集合

while count <= 3:
    pageurl = getData(pageurl, count, seen)
    count += 1
