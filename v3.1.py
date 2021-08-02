import pyautogui as pya
import collections
import sys
from time import sleep
import requests
import re
import win32gui
import win32con
import win32api
import win32clipboard

Point = collections.namedtuple('Point', 'x y')

url = 'https://forum.gamer.com.tw/C.php?page=999999&bsn=17532&snA=674866&tnum=13231'
headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36" }
duplicate = set()

def getText(choice):
    if choice == 2:
        try:
            with codecs.open('invitations.txt', 'r', 'utf-8') as f:
                s = f.read()
            if not s:
                raise Exception('\'invitations.txt\' 內容為空')
            return s, choice
        except Exception as e:
            print(e, '，將以爬蟲的方式獲取驗證碼')
    return requests.get(url, headers = headers).text, 1

def searchImg(img):
    temp = pya.locateOnScreen(img, confidence = 0.9)
    if temp == None:
        sys.exit(f'Image \"{img}\" not found.')
    return pya.center(temp)

def click(x, y):
    lParam = win32api.MAKELONG(x - windowRec[0], y - windowRec[1])
    win32gui.SendMessage(hwndChildList[4], win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.2)
    win32gui.SendMessage(hwndChildList[4], win32con.WM_LBUTTONUP, None, lParam)
    
def setText(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()
    
print('請輸入 Delay 的秒數:')
DELAY = float(input())
print('請輸入邀請碼取得方式 (1 為爬蟲，2 為讀取 \'invitations\')')
choice = int(input())

# 取得按鈕位置，若有偏差自行調整
pos = searchImg('button1.png')
textPos = Point(pos.x - 150, pos.y)
pya.click(textPos)
setText('LOLK938KR46XB')
pya.hotkey('ctrl', 'v')
pya.click(pos)
sleep(DELAY)

b1 = searchImg('button2.png')
pya.click(b1)
sleep(DELAY)

b2 = searchImg('button2.png')
pya.click(b2)
###

hwnd = win32gui.FindWindow(0, 'League Of Legends')
windowRec = win32gui.GetWindowRect(hwnd)

hwndChildList = []
win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
    
while True:
    s, choice = getText(choice)
    l = []

    for invitation in re.findall('LOL.{10}', s):
        if invitation.isalnum() and invitation not in duplicate:
            l.append(invitation)
            duplicate.add(invitation)
            
    if not l and choice == 1: continue

    if choice == 1:
        l = list(reversed(l))
    print(l)
    
    for s in l:
        sleep(DELAY)
        click(textPos.x, textPos.y)
        click(textPos.x, textPos.y)

        for c in s:
            vk = win32api.VkKeyScan(c)
            win32gui.PostMessage(hwndChildList[4], win32con.WM_KEYDOWN, vk, 0)
        
        sleep(DELAY)
        click(pos.x, pos.y)
        sleep(DELAY)
        click(b1.x, b1.y)
        sleep(DELAY)
        click(b2.x, b2.y)
        
    if choice == 2: break