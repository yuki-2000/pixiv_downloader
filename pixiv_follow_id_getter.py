# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:58:22 2021

@author: yuki
"""

from pixivpy3 import *
import json
import copy
from time import sleep
import datetime


#client.jsonの読み込み処理
f = open("client.json", "r")
client_info = json.load(f)
f.close()





#2021/2/21ログイン方法変更
#2021/11/9　api(PixivAPI())削除
aapi = AppPixivAPI()
aapi.auth(refresh_token = client_info["refresh_token"])





#現在のフォローユーザーのidを取得
server_ids = []
user_following = aapi.user_following(client_info["user_id"])
print("現在pixivであなたがフォローしているユーザーは")
while True:
    try:
        for i in range(30):
            server_ids.append(user_following.user_previews[i].user.id)
            print("{:<10}".format(user_following.user_previews[i].user.id) + user_following.user_previews[i].user.name)
        next_qs = aapi.parse_qs(user_following.next_url)
        sleep(1)
        user_following = aapi.user_following(**next_qs)
        sleep(1)
    except:
        print("\nたぶん終わり\n")
        break



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


