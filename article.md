https://qiita.com/yuki_2020/items/716fa4e4ada65306f688

の代わりです。
このようなことがあったので

![image](https://user-images.githubusercontent.com/88224293/236682006-6c2f0876-d84d-4c3c-a3fe-22f5284fbf4a.png)
https://twitter.com/tadanojako/status/1654676274089197568


# 2021/11/20追記　プログラムを一新し、記事の内容もほぼ書き直しました!!
2021/11/20以前公開していたプログラムをバージョン1.0、
今回新しくしたプログラムをバージョン2.0とします。
内容はほとんどすべて変わっていますので、１から記事を読んで環境を作ってください。

<!--

# 2021/11/7追記　現在この記事のプログラムは動きません。(解決済み)
どうやらpixiv側が`api = PixivAPI()`としていた`Public API`を無効化したようで、このapiを使用しているこの記事のプログラムは動かなくなりました。
`aapi = AppPixivAPI()`としているapiは使用できるので、こちらに移行中です。
プログラムができ次第、更新します。
しばしお待ちを。
-->
<!--
# 2021/2/21追記　ログイン方法を変えることで動くようになりました！！

https://qiita.com/yuki_2020/items/759e639a4cecc0770758

記事に従ってプログラムを変更してください。

今のこの記事のプログラムは変更していないので動きません。
自分で直してください。m(__)m
-->
<!--
# 2021/2/11追記　仕様変更によって現在動きません(解決済み)

https://github.com/upbit/pixivpy/issues/158

こちらに詳しいことがありますが、pixivpyはもともとandroidアプリを通してログインをしていましたが、
アップデートでログイン方法が変わったため、現在ログインできません。

```
PixivError: [ERROR] auth() failed! check username and password.
HTTP 400: {"has_error":true,"errors":{"system":{"message":"Invalid grant_type parameter or parameter missing","code":1508}},"error":"invalid_grant"}

```
こうなります。
とりあえず今はpixivpyの改良を待つか、
https://github.com/danbooru/danbooru/blob/39cc3ed5cf913499093d2f641d70d7682a14fa42/app/logical/pixiv_ajax_client.rb
こんなものが紹介されていたので、動くかわかりませんがrubyを勉強して試してみます。

-->

# はじめに

pixivからイラストをいちいち1枚ずつダウンロードするのは面倒くさいですよね
pythonを使って特定のユーザーの作品を自動でダウンロードできるプログラムを作りました。
画像だけでなく漫画、うごイラ、にも対応しています。
特にうごイラはそれぞれの画像をダウンロードし、gifも作成します。
タグや閲覧数による絞り込みや、ダウンロードする上限などを決めることができます。





# 注意

使用したライブラリ：pixivpy
中国語（オリジナル）

https://github.com/upbit/pixivpy

:::note warn
pixivpyはおそらく中国の有志が作ったライブラリであり、公式のものではありません。
そのためログイン時のユーザーid、passwordは流出してもいいように捨て垢を使うなどの方法を使うことをお勧めします。
:::

:::note warn
また乱用厳禁です。
スクレイピングのルールとして1秒当たりリクエリは1回までという暗黙のルールがあります。
これがないとdos攻撃となってしまい、法的にアウトです。
sleepをコメントアウトする際は自己責任でお願いします。
:::

:::note warn
また何か問題が起きても自己責任でお願いします。
:::














# 動作環境
このプログラムはwindows10環境下で動かしています。
Linux、Mac環境下で動作するかはわかりません。
2020/12/30現在でのanacondaの最新のバージョンで動きます
また、この記事はanaconda利用者向けに書きます。

* python3.8.5
* pixivpy3.5.10







# ダウンロード
## Anaconda
まずpythonを実行できるようにします。
おすすめはAnacondaをインストールすることです。
インストールの仕方は調べたらいろいろ出てくると思うので、ご自身で調べてください。
もちろん知識のある人はほかの方法でも問題ありません。


## ソースコード
プログラムはgithubに公開するようにしました。

https://github.com/yuki-2000/pixiv_downloader

使い方が分からない人、この画像のように、緑のCodeを押して、Download ZIPを押してください。その後適当な場所に解凍（展開）してください。


![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/18c528a9-607c-67fb-59eb-faa2db421ab4.png)




# ディレクトリ
ダウンロードすると、こんな感じになっています。

```
.
├── img
│   ├── 
├── chromedriver.exe
├── client.json
├── login_run.bat
├── pixiv_auth.py
├── pixiv_downloader.py
├── pixiv_downloader_tqdm.py
├── pixiv_follow_id_getter.py
├── pixiv_follow_id_getter_over5000.py
├── run.bat


```
画像だとこんな感じ
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/06cf363e-789b-8f11-6a37-ccad03fb9c56.png)







以後、バッチファイルを使用せずにコマンドプロンプトでプログラムを実行する人は、pythonを実行する前にこのディレクトリまで移動してください。

移動の仕方

https://kenchikku.com/archi-prog/py-a02/






# ライブラリのインストール

windowsの左下のスタートメニューを探すと、写真のようなAnaconda Prompt(anaconda3)というのがあるので、これを実行してください。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/eab8bc30-ba9b-8af4-520c-a826ea7a2c8d.png)

実行すると黒い画面が現れるので、

```
pip install pixivpy
```
と

```
pip install opencv-python
```

と入れて実行してください。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/ec1e62d6-5e08-3a9d-9b62-e8bc295454c5.png)


必用なライブラリがダウンロードされます。
インストールできないときは管理者でコマンドプロンプトを開いてやってみてください。
やり方は開くときに右クリックして「その他」→「管理者として実行」です。

http://y-okamoto-psy1949.la.coocan.jp/Python/Install35win/

また、この先何かライブラリがインストールされていないとエラーになったら、この方法でダウンロードしてください。



# バッチファイルの編集

コマンドラインで実行することに慣れているならやらなくていいです。
ただプログラミング初心者、ワンクリック、ドラックアンドドロップでプログラムを実行したい人はやってください。

バッチファイルの編集は、メモ帳などにバッチファイルをドラッグアンドドロップすることでできます。

`login_run.bat`、`run.bat`の2行目には、 

```.bat
call C:\Users\ユーザー\Anaconda3\Scripts\activate.bat
```
という記述があります。
anacondaをいじらずにインストールした人は、`ユーザー`となっているところを、windowsのユーザー名に変えるだけでいいです。
インストール先をいじった人はこのファイルの場所を探して絶対パスで記述してください。

詳しくは、こちらの記事で。

https://qiita.com/yuki_2020/items/dc6212b68f3d58bfe34d



# リフレッシュトークンの取得

ここにやり方は全部書いてあります。
__この記事の「前準備」の1～3のみ実行してください。__

https://qiita.com/yuki_2020/items/759e639a4cecc0770758

chromedriver.exeのバージョンを合わせたら`login_run.bat`をダブルクリックするだけで実行できます。

バッチファイルを使用しない人は、

```
python pixiv_auth.py login
```

で実行。
実行したら



```
❯ python3 pixiv_auth.py login
[INFO] Get code: 3s3Xc075wd7njPLJBXgXc4qS-...
access_token: Fp9WaXhNapC8myQltgEn...
refresh_token: uXooTT7xz9v4mflnZqJ...
expires_in: 3600
```

このように表示されるので、
`refresh_token: `
に続く`uXooTT7xz9v4mflnZqJ...`をコピーしてください（実際は「...」の部分はなく、長い文字列になっています。）


なお、__この文字列を使用してログインするので、ほかの人には見せないようにしましょう。__


# client.jsonの作成

ログイン用に使う情報を書いてください

```client.json
{
  "version": "20211117",
  "pixiv_id": "pixiv_id",
  "password": "password",
  "user_id": "0000000",
  "refresh_token": "abcdefg",
  "ids": [
  ]
}
```

## version
versionは更新した日付を表すだけなので、適当な数字でいいです。


## pixiv_id、password
"pixiv_id"、"password"は画像のところに普段入力している文字列です。
`pixiv_follow_id_getter_over5000.py`でのみ使用します。
`"pixiv_id": "12345"`のように""で囲って記述してください。

![ログイン.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/d45a813f-6a92-5b62-8503-315c98b44563.png)

## user_id
"user_id"は自分のuseridです。

![Inked画像1_LI.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/c70c6dab-f80c-a789-0514-f5c61912bab7.jpeg)

自分のユーザーのページに行き、urlの最後の番号です。


![InkedDesktop Screenshot 2020.12.31 - 21.22.03.74-1_LI.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/993303/3f918582-79d2-c144-35a6-26306ebe2bf8.jpeg)
https://www.pixiv.net/users/11
のようにあったら11です




## refresh_token
先ほどコピーしたrefresh_tokenをコピペしてください。
なお、__この文字列を使用してログインするので、ほかの人には見せないようにしましょう。__


## ids
ダウンロードするイラストレーターのuseridを記述しますが、`pixiv_follow_id_getter.py`で自動的に書き込むので触らないでください。（jsonとlistに理解があれば触ってもok）







# フォローしているユーザーのidの取得

`pixiv_follow_id_getter.py`を実行してください。
client.json内のidsにフォローしているidが書き込まれます。

なお実行は初回、新しくpixivでフォローしたときだけで、毎回実行しなくていいです。

実行方法は、`pixiv_follow_id_getter.py`をマウスでドラッグして、`run.bat`の上にドロップするだけです。

なおフォローしているユーザーが5000人を超えている場合はこのプログラムでは5000人までしか取得できないので、`pixiv_follow_id_getter_over5000.py`を代わりに実行してください。
実行方法は同じくマウスでドラッグして、`run.bat`の上にドロップするだけです。
5000人について、詳しくはこちらの記事をご覧ください。

https://qiita.com/yuki_2020/items/b0956ef9a48d51bf8bc1


参考までにコード

ログイン→
フォローを30人取得→
次の30人を取得→
最後まで行ったらclient.jsonに追加→




```pixiv_follow_id_getter.py
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

```














# イラストのダウンロード


ここまで来たらあと一歩。
`pixiv_downloader.py`マウスでドラッグして、`run.bat`の上にドロップするだけです。
なお、`pixiv_downloader_tqdm.py`は`pixiv_downloader.py`をもとに実行時このようなプログレスバー

```
#100%|██████████| 1000/1000 [01:39<00:00,  9.96it/s]
```

が表示されて見やすくしたプログラムです。
こちらのプログラムの実行のほうが分かりやすいです。
しかし意図しないミスがある可能性があります。

ただし、実行前に設定を各自で行ってもらいます。

```pixiv_downloaderもしくはpixiv_downloader_tqdmの上のほう.py
#設定
#ダウンロードする作品数
max_download_works=5
#ブックマーク数の最小値を設定
min_bookmarks=0
#閲覧数の最小値を設定
min_view=0
#コメント数
min_comments=0
#保存先
#画像を保存するディレクトリ
main_saving_direcory_path = "./img/"

#うごイラのダウンロード形式設定
#画質悪、ファイルサイズ大、ループ、保存場所は直下
ugoira_gif  = True
#画質良、ファイルサイズ小、ループしない（再生ソフト次第）、保存場所は直下
ugoira_mp4  = True
#画質最高（劣化なし）、ファイルサイズ小、ループ、ファイル移動できない（元の画像を参照しているため）、保存場所はugoiraフォルダ内
ugoira_html = True
#画質最高（劣化なし）、ループ、ファイルサイズ大、移動可、保存場所はugoiraフォルダ内
html_onefile = True

#Filter by tag　e.g. target_tag = ["Fate/GrandOrder","FGO","FateGO","Fate/staynight"]
select_tags = [] #同じtag内に複数書くと少なくとも一つあればダウンロード
select_tags2 = []#異なるタグ間のタグはすべて含まれていないとダウンロードされない
exclude_tags = ["R-18"]#一つでもかぶっていればダウンロードしない
```









プログラムを開き、個々のコメントにあるように設定してください
上記の状態では、R-18のタグが付いた作品を除く中から新しい順に5作品`./img/`にダウンロードされます。うごイラの場合はgifとmp4とhtmlが二つ作られます。
詳しく解説します。


## max_download_works
今回`max_download_works=5`となっていますが、これは新しい順に5作品（漫画などはまとめて1とカウント）ダウンロードされます。
なおすでにダウンロードされている画像もカウントします。
__ダウンロードする数を制限しない場合は`max_download_works=10000000000`など、膨大な数にしてください。__

## min_bookmarks、min_view、min_comments
それぞれの説明の通りの変数です。__0ではすべての作品をダウンロードします。__
例えば`min_bookmarks=100`とすればブックマークが100__未満__の作品はダウンロードされません。


## main_saving_direcory_path
画像の保存先です。デフォルトで`./img/`となっており、直下のimgフォルダに各イラストレーターさんのフォルダが作成され、その中にダウンロードされます。


## ugoira_*
作成したい形式は`True`、作成したくない形式は`False`としてください。

特徴は書いてある通りですが、gif、mp4、html、htmlの4種があります。
ぜひ一回うごイラをすべての形式でダウンロードして見比べてください。





|  | gif | mp4 | html | onefile |
|:-:|:-:|:-:|:-:|:-:|
| 画質  |  悪 | 良  | 無劣化  | 無劣化  |
| ファイルサイズ  | 大  | 小  | 小  | 大  |
| ループ  | あり  | なし  | あり  | あり  |
| 保存場所  | 直下  | 直下  | ugoiraフォルダ内  | ugoiraフォルダ内  |
|ファイル移動   | 可  | 可  | 不可  | 可  |
|その他  | 何となくおすすめ  | ループしないけどきれいな動画  | とりあえず無劣化で保存したいなら  | 無劣化で取り回しをよくしたいなら  |




なお、gif、htmlの作成は@choshicureさんの作った

https://qiita.com/choshicure/items/8795bf929e34af6622fc

を大変参考にさせていただきました。
ありがとうございました。


## tags
tagの挙動は面倒くさいです。
`select_tags = ["Fate/GrandOrder","FGO","FateGO","Fate/staynight"]`の時、
タグの中に「Fate/GrandOrder」 __または__「FGO」 __または__「FateGO」 __または__「Fate/staynight」が含まれていればダウンロードします。
さらに、
`select_tags = ["Fate/GrandOrder"]
select_tags2 = ["FGO"]`
の時は「Fate/GrandOrder」 __かつ__「FGO」が含まれている作品がダウンロードされます。

exclude_tagsは要素が一つでも含まれていたらダウンロードしません。
`exclude_tags = ["R-18","R-15"]`の場合、「R-18」 __または__「R-15」というタグが含まれていればダウンロードしません。





参考までに、`pixiv_downloader.py`のソースコードを書いておきます




ログイン→
設定→
各イラストレーターの処理→
フォルダの作成及びリネーム→
各イラストの処理→
ダウンロード可否の判断→
ダウンロード











```pixiv_downloader.py
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:34:20 2021

@author: yuki
"""

#今何枚目をダウンロードか表示したい
#明らかにgetの回数が増えたから全然進まない


from pixivpy3 import *
import json
import os
from PIL import Image
import glob
from time import sleep
import zipfile
import cv2
import numpy as np
import re


#client.jsonの読み込み処理
f = open("client.json", "r")
client_info = json.load(f)
f.close()


#2021/2/21ログイン方法変更
#2021/11/9　api(PixivAPI())削除
aapi = AppPixivAPI()
aapi.auth(refresh_token = client_info["refresh_token"])



#設定
#ダウンロードする作品数
max_download_works=5
#ブックマーク数の最小値を設定
min_bookmarks=0
#閲覧数の最小値を設定
min_view=0
#コメント数
min_comments=0
#保存先
#画像を保存するディレクトリ
main_saving_direcory_path = "./img/"

#うごイラのダウンロード形式設定
#画質悪、ファイルサイズ大、ループ、保存場所は直下
ugoira_gif  = True
#画質良、ファイルサイズ小、ループしない（再生ソフト次第）、保存場所は直下
ugoira_mp4  = True
#画質最高（劣化なし）、ファイルサイズ小、ループ、ファイル移動できない（元の画像を参照しているため）、保存場所はugoiraフォルダ内
ugoira_html = True
#画質最高（劣化なし）、ループ、ファイルサイズ大、移動可、保存場所はugoiraフォルダ内
html_onefile = True

#Filter by tag　e.g. target_tag = ["Fate/GrandOrder","FGO","FateGO","Fate/staynight"]
select_tags = [] #同じtag内に複数書くと少なくとも一つあればダウンロード
select_tags2 = []#異なるタグ間のタグはすべて含まれていないとダウンロードされない
exclude_tags = ["R-18"]#一つでもかぶっていればダウンロードしない


#ここから各イラストレーターさんごとの処理
#for user_id in [11,12848282]:
for user_id in client_info["ids"]:
    sleep(10)
    user_detail = aapi.user_detail(user_id)
    
    #主にmany access後の失敗でこちらに並ぶのでsleepを調節するとよい
    if "error" in user_detail:
        print(user_id)
        print(user_detail.error)

        sleep(60)
        #ここ関数化したら使えない
        continue
    
    
    user_name = user_detail.user.name
    total_works = user_detail.profile.total_illusts + user_detail.profile.total_manga

    #将来的に関数にするときのためにbreakを使わない
    if not total_works == 0:


        #フォルダパス作成
        directory_user_name = user_name
        #エスケープシーケンスを削除
        #https://pg-chain.com/python-escape
        directory_user_name = directory_user_name.translate((str.maketrans({'\n': '','\0': '','\t': '','\r': '',"\'": "'",'\"': '"', '\\':''})))
        #windowsで使えるフォルダ名に変更
        #https://www.itc.u-toyama.ac.jp/el/win7/restricted.html
        directory_user_name = directory_user_name.translate((str.maketrans({'/': '／' , ':': '：', '*': '＊', '?': '？', '"': "”", '>': '＞', '<': '＜', '|': '｜'})))
        #https://all.undo.jp/asr/1st/document/01_03.html
        #先頭ドット、末尾ドット
        directory_user_name = directory_user_name.strip(".")
        #半角スペース
        directory_user_name = directory_user_name.strip(" ")
        #全角スペース
        directory_user_name = directory_user_name.strip("　")
        saving_direcory_path = main_saving_direcory_path + directory_user_name + ("(") +str(user_id) + (")") + "/"

        #フォルダ名アップデート
        local_folders_list = glob.glob(main_saving_direcory_path + "*")
        for local_dir in local_folders_list:
            local_user_id = local_dir.rsplit("(", 1)[-1][:-1]
            local_user_name = os.path.basename(local_dir).rsplit("(", 1)[0]
            if local_user_id == str(user_id):
                if user_name != local_user_name:
                    print(local_dir + " を次に変更 " + saving_direcory_path)
                    os.rename(local_dir, saving_direcory_path)
                    sleep(3)
                break
        #フォルダ作成
        if not os.path.exists(saving_direcory_path):
            os.mkdir(saving_direcory_path)



        #ダウンロード開始
        #Display information of illustrator and the number of illustrations
        print("------------------------------------------------------------")
        print("start downloading " + str(total_works) + " illusts of {:<10}".format(user_id) + user_name)
        print("------------------------------------------------------------")
        
        

        next_qs=None
        download_work_no=0
        finish_flag=False

        #こちらでもいいが、めんどくさいのでwhile Trueで無限に回す
        #for i in range(total_works//30)
        
        #こことってこれないとぐるぐる回る
        user_illusts = aapi.user_illusts(user_id)
        while True:
            try:

                for illust in user_illusts.illusts:
                
                    #ダウンロード可否
                    #値で
                    if illust.total_bookmarks < min_bookmarks:
                        continue
                    if illust.total_view < min_view:
                        continue
                    if illust.total_comments < min_comments:
                        continue
                    
                    #タグで
                    illust_tags = []
                    for illust_tag in illust.tags:
                        illust_tags.append(illust_tag.name)
                    #タグが一つでも入っていたらダウンロード
                    #すべてのタグが入っているものだけを手に入れたかったらその分だけifを追加
                    if len(list(set(select_tags)&set(illust_tags))) == 0 and select_tags != []:
                        continue
                    if len(list(set(select_tags2)&set(illust_tags))) == 0 and select_tags2 != []:
                        continue
                    #excludeタグが一つでも入っていたらスキップ
                    if len(list(set(exclude_tags)&set(illust_tags))) > 0 :
                        continue


                    #ダウンロード済みか
                    #https://www.pixiv.help/hc/ja/articles/235584428-pixiv%E3%81%AB%E6%8A%95%E7%A8%BF%E3%81%A7%E3%81%8D%E3%82%8B%E7%94%BB%E5%83%8F%E3%81%AE%E7%A8%AE%E9%A1%9E%E3%82%92%E7%9F%A5%E3%82%8A%E3%81%9F%E3%81%84   
                    file_name_head = saving_direcory_path + str(illust.id)+"_p" + str(illust.page_count-1) 

                    if os.path.exists(file_name_head+".png") or os.path.exists(file_name_head+".jpg") or os.path.exists(file_name_head+".jpeg") or os.path.exists(file_name_head+".gif") or os.path.exists(saving_direcory_path+str(illust.id)+'_ugoira'):
                        print("--------------------------------")
                        print("Title:"+str(illust.title)+" has already downloaded.")
                        continue
                    
                    



                    


                    
                    #ダウンロード開始
                    sleep(1)
                    download_work_no += 1
                    print("--------------------------------")
                    print("download " + illust.title)
                    #print("caption")
                    print(illust.caption.replace("<br />", "\n"))




                    if illust.type == "illust":
                        if illust.page_count == 1:
                            aapi.download(illust.meta_single_page.original_image_url, saving_direcory_path)
                        else:
                            for page in illust.meta_pages:
                                aapi.download(page.image_urls.original, saving_direcory_path)
                                sleep(1)
                        


                    #うごイラ
                    #ページごとdelayが違ううごイラが作れない。今は1枚目のディレイを全体に適用
                    if illust.type == "ugoira":
                    #イラストIDの入力待機
                        illust_id = illust.id
                        ugoira_url = illust.meta_single_page.original_image_url.rsplit('0', 1)
                        ugoira = aapi.ugoira_metadata(illust_id)
                        ugoira_frames = len(ugoira.ugoira_metadata.frames)
                        ugoira_delay = ugoira.ugoira_metadata.frames[0].delay
                        fps = 1000 / ugoira_delay
                        height = illust.height
                        width = illust.width
                        dir_name = saving_direcory_path + str(illust_id)+'_ugoira'
                        
                        
                        #うごイラを保存するフォルダの作成
                        if not os.path.isdir(dir_name):
                            os.mkdir(dir_name)
                        
                        
                        #うごイラに使われているすべての画像のダウンロード(オリジナル) 
                        #高画質低速
                        for frame in range(ugoira_frames):
                            frame_url = ugoira_url[0] + str(frame) + ugoira_url[1]
                            aapi.download(frame_url, path=dir_name)
                            sleep(1)
                            
                        """                                               
                        #zipでダウンローのほうが速いが、低画質、動画がうまく作れない  
                        aapi.download(ugoira.ugoira_metadata.zip_urls.medium, path=dir_name)
                        print(os.path.join(dir_name, os.path.basename(ugoira.ugoira_metadata.zip_urls.medium)))
                        with zipfile.ZipFile(os.path.join(dir_name, os.path.basename(ugoira.ugoira_metadata.zip_urls.medium))) as existing_zip:
                            existing_zip.extractall(dir_name)
                        
                        
                        #ファイル名が数字のみなのでリネームする  jpg以外の画像あるのかわからない
                        frames = glob.glob(f'{dir_name}/*.jpg')
                        for frame in frames:
                            file_name = os.path.basename(frame)
                            #00000.jpgへの対策
                            file_name =file_name[:-5].lstrip("0") + file_name[-5:]
                            file_name = str(illust_id) + "_ugoira" + file_name
                            new_file = os.path.join(dir_name, file_name)
                            os.rename(frame, new_file)
                        """
                            
                        #jpg以外の画像あるのかわからない
                        frames = glob.glob(f'{dir_name}/*.jpg')
                        frames += glob.glob(f'{dir_name}/*.jpeg')
                        frames += glob.glob(f'{dir_name}/*.png')
                        #https://note.nkmk.me/python-sort-num-str/
                        frames.sort(key=lambda s: int(re.findall(r'\d+', s)[-1]))
                        #frames.sort(key=os.path.getmtime, reverse=False)
                        


                        
                        #保存した画像をもとにgifを作成
                        if ugoira_gif  == True:
                            ims = []
                            for frame in frames:
                                ims.append(Image.open(frame))
                            ims[0].save(f'{saving_direcory_path}/{illust_id}.gif', save_all=True, append_images=ims[1:], optimize=False, duration=ugoira_delay, loop=0)


                               
                        #動画の作成　opencv全角文字問題？ 
                        #なぜか作れる動画と作れない動画があると思ったら、zipの画像が元より小さい縦横の画像があることが判明
                        if ugoira_mp4  == True:
                            # encoder(for mp4)
                            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                            # output file name, encoder, fps, size(fit to image size)
                            video = cv2.VideoWriter(f'{saving_direcory_path}/{illust_id}.mp4',fourcc, fps, (width, height))
                            
                            for frame in frames:
                                #https://imagingsolution.net/program/python/opencv-python/read_save_image_files_in_japanese/
                                #numpyで開いてopencvに渡すことで全角文字のパスでも動く
                                buf = np.fromfile(frame, np.uint8)
                                img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
                                if img.shape[2] == 4:
                                    img = np.delete(img, 3, axis=2)
                                #img = cv2.imread(frame)
                                video.write(img)
                            
                            video.release()
                            #print('written')
                            
                            
                        #ローカルを参照するhtml
                        #https://qiita.com/choshicure/items/8795bf929e34af6622fc
                        if ugoira_html == True:

                            paths_json = json.dumps(frames)

                            html = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Document</title>
                            </head>
                            <body>
                                <canvas id="ugoira" width="{width}" height="{height}"></canvas>
                                <script>

                                    const paths = {paths_json};
                                    const images = paths.map(path => {{
                                        const image = new Image();
                                        image.src = path;
                                        return image;
                                        }});

                                    const canvas = document.querySelector('#ugoira');
                                    const context = canvas.getContext('2d');
                                    let count = 0;
                                    window.addEventListener('load', function(){{
                                        setInterval(function(){{
                                            context.clearRect(0, 0, canvas.width, canvas.height);
                                            context.drawImage(images[count], 0, 0);
                                            count++;
                                            if(count>={frames}) count=0;
                                        }}, {delay});
                                    }});
                                </script>
                            </body>
                            </html>
                            """.format(width=width, height=height, frames=ugoira_frames, illust_id=illust_id, delay=ugoira_delay, paths_json=paths_json)
                            with open(f'{dir_name}/ugoira.html', 'w', encoding='utf-8') as f:
                                f.write(html)
                                
                                
                        #一つのファイルにまとめたhtml
                        if html_onefile == True:
                            import base64
                            illust_b64 = []
                            img_ext = frames[0].split('.')[-1]
                            for frame in frames:
                                with open(frame, 'rb') as f:
                                    illust_b64.append(f'data:image/{img_ext};base64,{base64.b64encode(f.read()).decode()}')
                            html = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Document</title>
                            </head>
                            <body>
                                <canvas id="ugoira" width="{width}" height="{height}"></canvas>
                                <script>
                                    const illust_b64 = {illust_b64};
                                    const images = [];
                                    for(let i=0; i<{frames}; i++){{
                                        const img = new Image();
                                        img.src = illust_b64[i];
                                        images.push(img);
                                    }}
                                    const canvas = document.querySelector('#ugoira');
                                    const context = canvas.getContext('2d');
                                    let count = 0;
                                    window.addEventListener('load', function(){{
                                        setInterval(function(){{
                                            context.clearRect(0, 0, canvas.width, canvas.height);
                                            context.drawImage(images[count], 0, 0);
                                            count++;
                                            if(count>={frames}) count=0;
                                        }}, {delay});
                                    }});
                                </script>
                            </body>
                            </html>
                            """.format(width=width, height=height, frames=ugoira_frames, illust_id=illust_id, delay=ugoira_delay, illust_b64=str(illust_b64))
                            with open(f'{dir_name}/ugoira_onefile.html', 'w', encoding='utf-8') as f:
                                f.write(html)

                            

                        
                        

                    #max_download_worksに達したら2重ループをやめる
                    #https://note.nkmk.me/python-break-nested-loops/
                    if download_work_no >= max_download_works:
                        finish_flag=True
                        break
                
                
                if finish_flag == True:
                   break
               
                sleep(1)
                next_qs = aapi.parse_qs(user_illusts.next_url)
                if next_qs == None:
                    break
                    
                else:
                    sleep(1)
                    user_illusts = aapi.user_illusts(**next_qs)
                       


            except:
                print("error")
                import traceback
                traceback.print_exc()
                sleep(60)
                break
                #continueだとuser_illustsを新たにとってこれずエラーて回るのでbreakで次のユーザーにまわしちゃう

               
            
        print("-----------------------------")
        print("Download complete!　Thanks to {:<10}".format(user_id) + user_name)
        print()






```


# 使用時の注意

初めてダウンロードするときは時間がとてもかかります。
また、それによって通信がpixiv側から切断されてerroが出ることがあります。
そのようなときは時間を空けてもう一度実行してください。

R-18の作品については、ログインしたアカウントの設定で「表示しない」にしているとダウンロードされません。ダウンロードしたいときは一度pcでログインして設定してください。











# まとめ
今回はpythonを使ってユーザーの作品をフィルターをかけてダウンロードする方法を解説しました。
自分がこれを作り始めたきっかけは2、3年前に好きだった絵師さんが作品を全部消してしまったことがあったからです。
あの時全部ダウンロードしとけば、でも手動では時間が足りない、と思って作り出しました。
このプログラムを使えば作品のバックアップをできるようになります。
2年間自分で使ってみて、バグを直したり、gifダウンロードできるようにしたりしていました。
初期のころはユーザーさんが名前を変えると作品を全部ダウンロードしなおすこともあり、大変でした。
最近完成してきたかな、と思い公開しました。
追加してほしい機能、バグなどありましたらコメントしてください。
ありがとうございました。




# 今後
この方法だと、毎回pixivのサーバーに負荷がかかりすぎてしまうから新着からダウンロードするように改造したい

バージョン2.0を作るにあたり、新しくしたことなど近々記事を書く予定です。

2021/1/14追記
書きました。

https://qiita.com/yuki_2020/items/4c2031cc359fdcab7e6e

# 参考にしたサイト



https://qiita.com/Hirosaji/items/304de7508df4b1cae904

https://www.mathgram.xyz/entry/scraping/pixiv

https://qiita.com/choshicure/items/8795bf929e34af6622fc

https://qiita.com/Mechanetai/items/1c59ba627ebc1654868d

https://ithikawa.hatenablog.com/entry/2018/11/11/203125

https://qiita.com/Hirosaji/items/304de7508df4b1cae904



# 兄弟記事

https://qiita.com/yuki_2020/items/acad0a1e1939dccdde59

https://qiita.com/yuki_2020/items/716fa4e4ada65306f688

https://qiita.com/yuki_2020/items/46b10da6e59bad573c1a

https://qiita.com/yuki_2020/items/efe6eda433b09ec34203

https://qiita.com/yuki_2020/items/759e639a4cecc0770758

https://qiita.com/yuki_2020/items/b0956ef9a48d51bf8bc1







