import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter
#RANGE 0DAN X EKADAR OLACAK STRİNG BİRLEŞTİRİP EKLENECEK
index=1
flag=0
outWorkbook=xlsxwriter.Workbook("Lİse&UniversiteHazırlık.xlsx")
outSheet=outWorkbook.add_worksheet()
outSheet.write("A1","İsim Soyisim")
outSheet.write("B1","Numara")
outSheet.write("C1","Branş")

#sadece url ile urldegisi degistirp forun şeyi 50den fazlaysa 50 50den azsa x yapıyoruz
#agent ne işe yarıyor öğren
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
urlmain="https://www.sahibinden.com"
url="https://www.sahibinden.com/ozel-ders-verenler-lise-universite-hazirlik?pagingOffset=0"
urldegis="https://www.sahibinden.com/ozel-ders-verenler-lise-universite-hazirlik?pagingOffset="
r=requests.get(url, headers=agent)
soup=BeautifulSoup(r.content,"html.parser")
string=str(soup.find("p",attrs={"class":"mbdef"}))
x=int(re.search(r'\d+', string).group())

if(x>50):
    x=50

for i in range(0,x):
    print("Sayfa numarası=",i)
    agent = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    urlsayfa=urldegis+str(i*20)
    r = requests.get(urlsayfa, headers=agent)
    soup = BeautifulSoup(r.content, "html.parser")
    hocalar=soup.find_all(attrs={"class","classifiedTitle"})


    for hoca in hocalar:
        agent = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        urlnew=urlmain+hoca.get("href")
        print(urlnew)
        r = requests.get(urlnew, headers=agent)
        sou = BeautifulSoup(r.content, "html.parser")
        print(sou.find("div",attrs={"class":"username-info-area"}).text)
        isim=sou.find("div",attrs={"class":"username-info-area"}).text
        outSheet.write(index,0,isim)
        if(sou.find("span",attrs={"class":"pretty-phone-part"})!=None):
            print(sou.find("span",attrs={"class":"pretty-phone-part"}).text)
            numara=sou.find("span",attrs={"class":"pretty-phone-part"}).text
            outSheet.write(index,1,numara)
            flag=1
        dersler = sou.find_all("li", attrs={"class": "selected"})
        bra=""
        count=1
        for ders in dersler:
            #print(ders.text)
            brans=ders.text.strip()
            if count==1:
                bra=brans
            else:
                bra=bra+", "+brans
            count+=1
        print(bra)
        outSheet.write(index, 2, bra)
        if(flag==1):
            index += 1
            flag=0
outWorkbook.close()


