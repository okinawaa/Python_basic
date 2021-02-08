import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}

# url 은 계속 변할것이다 페이지가변할것이기에

for i in range(1,6):
    # print(" 페이지 : " , i )
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={0}&rocketAll=false&searchIndexingToken=&backgroundColor=".format(i)
    res = requests.get(url,headers = headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text , "lxml")

    items = soup.find_all("li",attrs={"class" : re.compile("^search-product")})
    #print(items[0].find("div",attrs={"class":"name"}).get_text())
    for item in items:

        ad_badge = item.find("span",attrs={"class":"ad-badge-text"})
        if ad_badge:
            # print("광고 상품 표시안함")
            continue

        name = item.find("div", attrs={"class":"name"}).get_text() # 제품명

        # 애플 제품 제외
        if "Apple" in name:
            # print(" <Apple 상품 제외합니다>")
            continue

        price = item.find("strong", attrs={"class":"price-value"}).get_text()
        rate = item.find("em",attrs={"class":"rating"})
        if(rate):
            rate = rate.get_text()
        else:
            # print("평점(이) 가 없습니다")
            continue

        rate_cnt = item.find("span",attrs={"class":"rating-total-count"})
        if(rate_cnt):
            rate_cnt = rate_cnt.get_text()
            rate_cnt = rate_cnt[1:-1]
        else:
            # print("리뷰가 없습니다")
            continue

        # if (float(rate) >= 4.5) and (int(rate_cnt) >= 50):
        #     print("{0} \n {1} \n {2} \n {3} \n".format(name,price,rate,rate_cnt))
        
        link = item.find("a" , attrs = {"class":"search-product-link"})["href"]
        if float(rate) >= 4.5 and int(rate_cnt) >= 100:
            print(f"제품명 : {name}")
            print(f"가격 : {price}")
            print(f"평점 : {rate}점 ({rate_cnt})")
            print("바로가기 : {}".format("https://www.coupang.com" + link))
            print("-"*100) # 줄긋기
    