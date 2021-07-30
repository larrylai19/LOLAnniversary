import pyautogui as pya
import collections
import sys
from time import sleep
import requests
import re

Point = collections.namedtuple('Point', 'x y')
pya.FAILSAFE = True

DELAY = 0.8
url = 'https://forum.gamer.com.tw/C.php?page=999999&bsn=17532&snA=674866&tnum=13231'
headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36" }
duplicate = set()

def searchImg(img):
    temp = pya.locateOnScreen(img, confidence = 0.9)
    if temp == None:
        sys.exit(f'Image \"{img}\" not found.')
    return pya.center(temp)

# 取得按鈕位置，若有偏差自行調整
pos = searchImg('button1.png')
textPos = Point(pos.x - 150, pos.y)
pya.click(textPos)
pya.typewrite('LOLK938KR46XB')
pya.click(pos)
sleep(DELAY)

b1 = searchImg('button2.png')
pya.click(b1)
sleep(DELAY)

b2 = searchImg('button2.png')
pya.click(b2)
###

while True:
    req = requests.get(url, headers = headers)
    l = []

    for s in re.findall('LOL.{10}', req.text):
        if s.isalnum() and s not in duplicate:
            l.append(s)
            duplicate.add(s)
            
    if not l: continue

    l = list(reversed(l))
    print(l)
    
    for s in l:
        sleep(DELAY)
        pya.click(textPos)
        pya.hotkey('ctrl', 'a')
        pya.typewrite(s)
        pya.click(pos)
        sleep(DELAY)
        pya.click(b1)
        sleep(DELAY)
        pya.click(b2)