# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:10:40 2020

@author: yuki
"""

#1.3.1を前提に配布用に変更
#aapiではフォローユーザー5000人以降はとってこれないのでwebからスクレイピングする





from pixivpy3 import *
import json
import copy
from time import sleep
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tqdm import tqdm



f = open("client.json", "r")
client_info = json.load(f)
f.close()


#2021/2/21ログイン方法変更
#2021/11/9　api(PixivAPI())削除
aapi = AppPixivAPI()
aapi.auth(refresh_token = client_info["refresh_token"])



#フォロー数の確認
user_detail = aapi.user_detail(client_info["user_id"])
total_follow_users = user_detail.profile.total_follow_users
print("全部で"+ str(total_follow_users) + "人フォローしています")
total_follow_page = total_follow_users//24 +1



#ここからseleniumでのid取得
options = Options()
# Headlessモードを無効にする（Trueだとブラウザが立ち上がらない）
options.set_headless(False)


# ブラウザを起動する
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
driver.get("https://accounts.pixiv.net/login")

login_id = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
login_id.send_keys(client_info["pixiv_id"])
password = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
password.send_keys(client_info["password"])

login_btn = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')
login_btn.click()

#ネット回線が遅くてログイン完了前にページ遷移してエラーになってしまうならここを長くする
sleep(4)



server_ids = []
for i in range(1, total_follow_page+1):

    #ログインページに
    url = "https://www.pixiv.net/users/" +str(client_info["user_id"]) + "/following?p={}".format(i)
    driver.get(url)
    
    #表示前に処理を始めないように一応
    sleep(2)
    
    html = driver.page_source.encode('utf-8')
    #print(html)
    #https://hideharaaws.hatenablog.com/entry/2016/05/06/175056
    #lxmlだとなぜが取得的ないページが
    soup = BeautifulSoup(html, "html5lib")
    #ここのclass_は前回と変わったので定期的にチェックを    
    users = soup.find_all("div", class_ = "sc-19z9m4s-5 iqZEnZ")

    
    for user in users:        
        url = user.find("a")["href"]        
        user_id = url.split("/")[-1]
        user_name = user.find("a").text
        print("{:<10}".format(user_id) + user_name)
        server_ids.append(user_id)
    

    





#ここからは、pixivでフォロー解除したユーザーについて、client_infoから削除しないようにする処理
#もしくはエラーで取得できなかったユーザーを削除しないように

#現在のjsonと比較して追加したい
#listはオブジェクトだからメモリの位置が渡されてしまうからcopyを使う
new_ids = copy.copy(client_info["ids"])
for i in range(len(server_ids)):
    if (server_ids[i] not in client_info["ids"]):
        new_ids.append(server_ids[i])
        print("{:<10}".format(server_ids[i]) + "を追加したよ")

#数値を表示したい
print("現在のフォロー総数は")
print(len(server_ids))
print("更新前のリスト内の総数は")
print(len(client_info["ids"]))
print("更新後のリスト内の総数は")
print(len(new_ids))

#for i in range(len(new_ids)):
    #print(new_ids[i] not in client_info["ids"])


#client.jsonに書き込みたい
client_info["ids"] = new_ids
client_info["version"] = datetime.datetime.now().strftime('%Y%m%d')

with open("client.json", "w") as n:
    json.dump(client_info, n, indent=2, ensure_ascii=False)




#これid取得時に逐次比較のほうがメモリ的にもよくね？


