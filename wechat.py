# https://itchat.readthedocs.io/zh/latest/
import time
import itchat
import requests
import ctypes

# 权限好友
allow_friends_list = []

info = """说明：
•功能
    1.查天气 “天气 城市名”
        如 “天气 北京市”
    2.下载网易云歌曲 “网易云下载 歌曲ID”
        如 “网易云下载 12121212”
    3.高清风景图 “随机风景”
    4.更换电脑随机桌面壁纸 ”换桌面“(不对外开放)
        注意 本功能仅限作者授权的好友
        ”换桌面 返回壁纸“可以向你发送这次的壁纸
•注意
    本功能不可商用 如要商用请联系作者
    邮箱:2756558228@qq.com"""


# 天气
def weather_message(s):
    city = s[3:]
    print("查天气", city)
    resp = requests.get(f"https://api.vvhan.com/api/weather?city={city}")
    print(resp)
    a = resp.json()
    if resp.json()["success"]:
        message = f"天气查询:\n" \
                  f"城市:{a['city']}\n" \
                  f"{a['info']['date']}天气:{a['info']['type']}\n" \
                  f"最高温度:{a['info']['high'][3:]}  最低温度:{a['info']['low'][3:]}\n" \
                  f"风向:{a['info']['fengxiang']}  风力:{a['info']['fengli']}\n" \
                  f"生活提示:{a['info']['tip']}"
        return str(message)
    else:
        return "请求失败,请检查城市名格式"


def set_img_as_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)


picurl = 'https://api.vvhan.com/api/bing?type=sj'


def get_reply(keyword):
    try:
        url = f"https://open.drea.cc/bbsapi/chat/get?keyWord={keyword}&userName=type%3Dbbs"
        res = requests.get(url)
        data = res.json()
        return data['data']['reply']
    except:
        return "opps, 我还很笨，不造你在说啥"


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def print_content(msg):
    print(msg.FromUserName + "发送了" + msg.Content)
    s = msg['Text']

    if s == "说明":
        itchat.send(info, msg.FromUserName)
    elif s[0:2] == "天气":
        itchat.send(weather_message(msg['Text']), msg.FromUserName)

    elif s[0:5] == "网易云下载":
        # print("网易云下载", s[6:])
        url = f"http://music.163.com/song/media/outer/url?id={s[6:]}.mp3"
        resp = requests.get(url)
        # print(resp)
        with open(f"./wangyi_music/{s[6:]}.mp3", mode="wb") as f:
            itchat.send("正在下载...", msg.FromUserName)
            f.write(resp.content)
        itchat.send("正在发送", msg.FromUserName)
        itchat.send_file(f"./wangyi_music/{s[6:]}.mp3", msg.FromUserName)

    elif s == "随机风景":
        # print("风景下载", s[6:])
        url = "https://api.vvhan.com/api/view"
        resp = requests.get(url)
        # print(resp)
        t = time.time()
        with open(f"./fengjing/{t}.jpg", mode="wb") as f:
            itchat.send("正在下载...", msg.FromUserName)
            f.write(resp.content)
        itchat.send("正在发送", msg.FromUserName)
        itchat.send_image(f"./fengjing/{t}.jpg", msg.FromUserName)

    # 更换壁纸 用户合法
    elif s[0:3] == "换桌面" and msg.FromUserName in allow_friends_list:
        resp = requests.get(picurl)
        path = f'E:/Code/pythonProject/杂七杂八/微信助手/Bing_pic/{str(time.time()).replace(".", "")}.jpg'
        with open(path, 'wb') as f:
            f.write(resp.content)
        set_img_as_wallpaper(path)
        print("通过权限检查，已更换壁纸。")
        itchat.send("通过权限检查，已更换壁纸。", msg.FromUserName)
        if s[4:] == "返回壁纸":
            itchat.send_image(path, msg.FromUserName)

    # 更换壁纸 用户不合法
    elif s[0:3] == "换桌面" and msg.FromUserName not in allow_friends_list:
        itchat.send("未通过权限检查 请联系作者添加\nErrormessage:Not in allow_frinds_list", msg.FromUserName)
        print("未通过权限检查 请联系作者添加\nErrormessage:Not in allow_frinds_list")

    # 其余自动回复
    else:
        reply = "execuse me?"
        try:
            reply = get_reply(msg.text)
        except:
            pass
        finally:
            print(f'[In] {msg.text} \t [Out] {reply}')
            return reply


itchat.auto_login()
itchat.run()