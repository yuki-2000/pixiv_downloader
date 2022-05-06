# pixiv_downloader2.0
pythonのライブラリ「pixivpy」を使用したダウンローダー

## 環境
windows、anaconda、chromeを前提に作成しています。  
`pip install pixivpy`  
で非公式ライブラリをダウンロードして使用します。  
その他必要なライブラリは自分自身でダウンロードしてください。  

## 注意
chromedriverはver96時点のものです。
バージョンが違うと動かないので、各自ダウンロードしてください。
https://qiita.com/yuki_2020/items/759e639a4cecc0770758#3chromedriverexe%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84

run.bat、login_run.batは
https://qiita.com/yuki_2020/items/dc6212b68f3d58bfe34d
を参考に2行目を自分のパソコンのパスにしてください

## 使い方

詳しくは  
https://qiita.com/yuki_2020/items/716fa4e4ada65306f688
を見てください。  



1.pixiv_auth.pyを実行してください。  
login_run.batをダブルクリックするか、コマンドラインで引数で「login」を渡してください。  
そしてrefresh_tokenをメモって下さい。

2.client.jsonに必要事項書き込んでください。

3.pixiv_follow_id_getter.pyを実行してフォローユーザー一覧を取得  
pixiv_follow_id_getter_over5000.pyはフォローユーザーが5000人以上いるときのみ使用してください。

4.pixiv_downloader.pyを実行してダウンロードする。  
pixiv_downloader_tqdm.pyはpixiv_downloader.pyをもとに実行時見やすくしたプログラムです。
しかし意図しないミスがある可能性があります。

