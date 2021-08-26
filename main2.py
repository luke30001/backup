from os import replace
#from typing import Text
import requests
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime
#from requests.api import get
import telebot
from telebot import types
import os
import urllib
fid=-1001503051596
username = "o_1eg6v1l7qc"
password = "Napoli101@"
maxdesc=20
TAG_RE = re.compile(r'<[^>]+>')
cid=-1001401024374
end=20 #22
start=5 #7
bot=telebot.TeleBot("1144044250:AAFk93xAVG7g3_okHFVU6w9UUlTTb6dhTag")
def rmhtml(text):
    return TAG_RE.sub('', text)
def getlast(url):
    #link=requests.get("https://www.pepper.it/codici-sconto/amazon.it?thread_type_translation=codici-sconto&page=1&threadTypeId=1&show-expired=0",headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}).text.split("https:\/\/www.pepper.it\/offerte\/")[1].split('"')[0]
    #linkoff="https://www.pepper.it/offerte/"+link[:len(link)-1]
    #print(link)
    #print(requests.get(url).headers)
    linkoff=BeautifulSoup(requests.get(url).text, 'html.parser').find_all("a", {"class": "cept-tt thread-link linkPlain thread-title--list"})[0]['href']
    return linkoff
def grabasin(l):
    asin = re.search(r'/[dg]p/([^/]+)', l, flags=re.IGNORECASE).group(1).split('?')[0]
    return asin
def gett():
    return(datetime.today().strftime('%Y-%m-%d'))
def read(file):
    try:
        f = open(file, "r")
        r=f.read()
        f.close()
        return r
    except:
        return ""
def write(file,txt):
    f = open(file, "w+")
    f.write(txt)
    f.close()
def append(file,txt): 
    write(file,read(file)+txt)
def getlastasin(file):
    try:
        lista=read(file)
        l=len(lista)-10
        return(lista[l:])
    except:
        return("")
def getlistasin():
    return requests.get("https://prezzone97.altervista.org/programma/file").text
def check(l):
    asin=grabasin(l)
    lista=getlistasin()
    if(asin not in lista):
        return True
    else:
        return False
def shortdesc(text):
    desc=text.split(' ')
    print(desc)
    ii=0
    dd=""
    tt=True
    for v in desc:
        ii=ii+1
        if (ii<maxdesc):
            if(dd==""):
                dd=v
            else:
                dd=dd+" "+v
        else:
            if(tt):
                tt=False
                dd=dd+"..."
    return dd
def imgzer(l):
    return requests.get("https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=IT&ASIN="+grabasin(l)+"&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_AC_SX466_").url
def issetclass(v):
    try:
        v["class"]
        return True
    except:
        return False
def getinfo(url):
    html=BeautifulSoup(requests.get(url).text, 'html.parser')
    de=rmhtml( html.find_all("div",{"class":"cept-description-container overflow--wrap-break width--all-12 space--mt-3 overflow--hidden"})[0].decode_contents()).strip()
    p=html.find_all("span",{"class":"thread-price text--b cept-tp size--all-l size--fromW3-xl"})[0].decode_contents()
    n=html.find_all("span",{"class":"thread-title--item"})[0].decode_contents()
    op=html.find_all("span",{"class":"mute--text text--lineThrough size--all-l size--fromW3-xl cept-next-best-price"})
    if(len(op)>0):
        op=op[0].decode_contents()
    else:
        op=None
    d=html.find_all("span",{"class":"space--ml-1 size--all-l size--fromW3-xl cept-discount"})
    if(len(d)>0):
        d=d[0].decode_contents()
    else:
        d=None
    c=html.find_all("input",{"class":"lbox--v-4 flex--width-calc-fix flex--grow-1 overflow--ellipsis width--all-12 hAlign--all-c text--color-charcoal text--b btn--mini clickable"})
    if(len(c)>0):
        c=c[0]["value"]
    else:
        c=None
    l=html.find_all("a")
    for v in l:
        if(issetclass(v)):
            if("cept-dealBtn" in v["class"]):
                l=v["href"]
    print(l)
    l=requests.get(l).url
    ts=check(l)
    a=grabasin(l)
    #i=imgzer(l)
    i=""
    lu=l
    l="https://www.amazon.it/dp/"+grabasin(l)+"/?tag=prezzone97-21"
    return({"name":n,"last":url,"description":shortdesc(de),"price":p,"oldprice":op,"discount":d,"coupon":c,"link":l,"image":i,"asin":a,"oldlink":lu,"tosend":ts})
def notdisturb():
    now = int(datetime.now().hour)
    print(now)
    if(now>start and now<end):
        return True
    else:
        return False
def getimg(url):
    print(url)
    f = open('image.jpg','wb')
    f.write(requests.get(url).content)
    f.close()
def addasin(asino):
    payloado={"txt":asino,"pswd":"Napoli101@"}
    requests.post("https://prezzone97.altervista.org/programma/write.php",data=payloado)
def send_site(info):
    payload={"name":info["name"],"desc":info["description"],"price":info["price"],"oldprice":info["oldprice"],"disc":info["discount"],"coupon":info["coupon"],"link":info["link"],"image":info["image"],"asin":info["asin"],"pswd":"Napoli101@"}
    requests.post("https://prezzone97.altervista.org/index.php",data=payload)
def shortn(url):
    #auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
    #access_token = auth_res.content.decode()
    access_token="25d0c560bcc0131c019b949ab583adb1d58f63e3"
    print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
    print(groups_res.text)
    groups_data = groups_res.json()['groups'][0]
    guid = groups_data['guid']
    shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid,"domain": "bit.ly", "long_url": url}, headers=headers)
    link = shorten_res.json().get("link")
    return(link)
def geturl(info):
    cc=""
    if(info["coupon"]==None):
        cc=""
    else:
        cc=info["coupon"]
    return shortn("https://affarone97.wixsite.com/prezzone/redirecting?img="+urllib.parse.quote(str(info["image"]))+"&url="+urllib.parse.quote(str(info["link"]))+"&name="+urllib.parse.quote(str(info["name"])))
def addlast(last):
    requests.post("https://prezzone97.altervista.org/programma2/write.php",data={"pswd":"Napoli101@","txt":last}).text
def send_offer(info):
    markup = types.InlineKeyboardMarkup()
    lo=geturl(info)
    itembtna = types.InlineKeyboardButton('Vai!',url=lo)
    markup.row(itembtna)
    getimg(info["image"])
    img = open('image.jpg', 'rb')
    disc=int(info["discount"].replace("%",""))
    if(disc<50):
        bot.send_photo(cid,img,caption="""⚠️PREZZONE⚠️
"""+info["name"]+"""

📝"""+info["description"]+"""📝

💶PREZZO:<b>"""+info["price"]+"""</b>💶:(invece di:💰<b>"""+info["oldprice"]+"""</b>💰)

SCONTO:📉<b>"""+info["discount"]+"""</b>📉""", reply_markup=markup,parse_mode="html")
    else:
        bot.send_photo(cid,img,caption="""🔥AFFARONE🔥
"""+info["name"]+"""

📝"""+info["description"]+"""📝

💶PREZZO:<b>"""+info["price"]+"""</b>💶:(invece di:💰<b>"""+info["oldprice"]+"""</b>💰)

SCONTO:📉<b>"""+info["discount"]+"""</b>📉""", reply_markup=markup,parse_mode="html")
    getimg(info["image"])
    img = open('image.jpg', 'rb')
    if(info["coupon"]!=None):
        bot.send_message(cid,info["coupon"])
        bot.send_photo(fid,img,caption="""💶PREZZO:<b>"""+info["price"]+"""</b>💶:(invece di:💰<b>"""+info["oldprice"]+"""</b>💰)

SCONTO:📉<b>"""+info["discount"]+"""</b>📉

🛍️"""+info["name"]+"""🛍️

📝"""+info["description"]+"""📝""", reply_markup=markup,parse_mode="html")
    else:
        bot.send_photo(fid,img,caption="""💶PREZZO:<b>"""+info["price"]+"""</b>💶:(invece di:💰<b>"""+info["oldprice"]+"""</b>💰)

SCONTO:📉<b>"""+info["discount"]+"""</b>📉 con coupon 🎟️"""+info["coupon"]+"""🎟️

🛍️"""+info["name"]+"""🛍️

📝"""+info["description"]+"""📝""", reply_markup=markup,parse_mode="html")
    img.close()
    send_site(info)
    addasin(info["asin"])
    addlast(info["last"])
def checklast(last):
    if(last in requests.get("https://prezzone97.altervista.org/programma2/file").text):
        return False
    else:
        return True
while(True):
    if(notdisturb()):
        linkoff=getlast("https://www.pepper.it/codici-sconto/amazon.it")
        print(linkoff)
        if(checklast(linkoff)):
            print(linkoff)
            info=getinfo(linkoff)
            print(info)
            if(info["tosend"]):
                info["image"]=imgzer(info["oldlink"])
                send_offer(info)
    time.sleep(60)