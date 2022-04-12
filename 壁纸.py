import ctypes
import requests
import time


def set_img_as_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)


url = 'https://api.vvhan.com/api/bing?type=sj'
resp = requests.get(url)
path = f'E:/Code/pythonProject/杂七杂八/壁纸助手/Bing_pic/{str(time.time()).replace(".", "")}.jpg'
with open(path, 'wb') as f:
    f.write(resp.content)
set_img_as_wallpaper(path)
