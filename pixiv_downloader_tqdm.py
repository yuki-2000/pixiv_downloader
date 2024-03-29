# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:34:20 2021

@author: yuki
"""

#今何枚目をダウンロードか表示したい
#明らかにgetの回数が増えたから全然進まない
#うごイラ最後までダウンロードした？


from pixivpy3 import *
import json
import os
from PIL import Image
import glob
from time import sleep
import zipfile
import cv2
import numpy as np
from tqdm import tqdm
#https://www.kimoton.com/entry/20190830/1567128952
import re


#https://qiita.com/yuki_2020/items/cdab3b0ce451bc9e3179
def rename_for_windows(name):
    while True:
        tmp = name
        #半角文字の削除        
        name = name.translate((str.maketrans({'\a':'','\b':'','\f':'','\n':'','\r':'','\t':'','\v':'',"\'":"'",'\"':'"','\0':''})))    
        #エスケープシーケンスを削除
        name = name.translate((str.maketrans({'\\':'￥','/': '／' , ':': '：', '*': '＊', '?': '？', '"': "”", '>': '＞', '<': '＜', '|': '｜'})))
        #先頭/末尾のドットの削除 
        name = name.strip(".")
        #先頭/末尾の半角スペースを削除
        name = name.strip(" ")
        #先頭/末尾の全角スペースを削除
        name = name.strip("　")

        if name == tmp:
            break

    return name


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
#画質最高（劣化なし）、ループ、ファイルサイズ大、移動可、保存場所は直下、delayが正確
html_onefile = True

#Filter by tag　e.g. target_tag = ["Fate/GrandOrder","FGO","FateGO","Fate/staynight"]
select_tags = [] #同じtag内に複数書くと少なくとも一つあればダウンロード
select_tags2 = []#異なるタグ間のタグはすべて含まれていないとダウンロードされない
exclude_tags = ["R-18","R-18G"]#一つでもかぶっていればダウンロードしない


#ここから各イラストレーターさんごとの処理
#for user_id in tqdm([11,12848282], desc='users', leave=False):
for user_id in tqdm(client_info["ids"], desc='users', leave=False):
    
    sleep(10)
    user_detail = aapi.user_detail(user_id)
    

    #主にmany access後の失敗でこちらに並ぶのでsleepを調節するとよい
    if "error" in user_detail:
        #print(user_id)
        #print(user_detail.error)
        tqdm.write(str(user_id))
        tqdm.write(str(user_detail.error))
        sleep(60)
        #ここ関数化したら使えない
        continue

    
    user_name = user_detail.user.name
    total_works = user_detail.profile.total_illusts + user_detail.profile.total_manga

    #将来的に関数にするときのためにbreakを使わない
    if not total_works == 0:


        #フォルダパス作成
        directory_user_name = user_name
        directory_user_name = rename_for_windows(directory_user_name)
        saving_direcory_path = main_saving_direcory_path + directory_user_name + ("(") +str(user_id) + (")") + "/"

        #フォルダ名アップデート
        local_folders_list = glob.glob(main_saving_direcory_path + "*")
        for local_dir in local_folders_list:
            local_user_id = local_dir.rsplit("(", 1)[-1][:-1]
            local_user_name = os.path.basename(local_dir).rsplit("(", 1)[0]
            if local_user_id == str(user_id):
                if user_name != local_user_name:
                    #print(local_dir + " を次に変更 " + saving_direcory_path)
                    tqdm.write(local_dir + " を次に変更 " + saving_direcory_path)
                    os.rename(local_dir, saving_direcory_path)
                    sleep(3)
                break
        #フォルダ作成
        if not os.path.exists(saving_direcory_path):
            os.mkdir(saving_direcory_path)



        #ダウンロード開始
        #Display information of illustrator and the number of illustrations
        tqdm.write("------------------------------------------------------------")
        tqdm.write("start downloading " + str(total_works) + " illusts of {:<10}".format(user_id) + user_name)
        tqdm.write("------------------------------------------------------------")
        #print("------------------------------------------------------------")
        #print("start downloading " + str(total_works) + " illusts of {:<10}".format(user_id) + user_name)
        #print("------------------------------------------------------------")
        
        

        next_qs=None
        download_work_no=0
        finish_flag=False

        
        
        #こことってこれないとぐるぐる回る
        user_illusts = aapi.user_illusts(user_id, type=None)
        #こちらでもいいが、めんどくさいのでwhile Trueで無限に回す
        for i in tqdm(range(total_works//30), desc='pages', leave=False):
        #while True:
            try:

                for illust in tqdm(user_illusts.illusts, desc='illusts', leave=False):
                
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

                    if os.path.exists(file_name_head+".png") or os.path.exists(file_name_head+".jpg") or os.path.exists(file_name_head+".jpeg") or os.path.exists(file_name_head+".gif"):
                        tqdm.write("--------------------------------")
                        tqdm.write("Title:"+str(illust.title)+" has already downloaded.")
                        #print("--------------------------------")
                        #print("Title:"+str(illust.title)+" has already downloaded.")
                        continue
                    
                    

                    file_name_head = saving_direcory_path + str(illust.id)
                    if (ugoira_gif==False or os.path.exists(file_name_head+".gif")) and (ugoira_mp4==False or os.path.exists(file_name_head+".mp4")) and (html_onefile==False or os.path.exists(file_name_head+".html")):
                        tqdm.write("--------------------------------")
                        tqdm.write("Title:"+str(illust.title)+" has already downloaded.")
                        #print("--------------------------------")
                        #print("Title:"+str(illust.title)+" has already downloaded.")
                        continue

                    


                    
                    #ダウンロード開始
                    sleep(1)
                    download_work_no += 1
                    tqdm.write("--------------------------------")
                    tqdm.write("download " + illust.title)
                    #tqdm.write("caption")
                    tqdm.write(illust.caption.replace("<br />", "\n"))
                    #print("--------------------------------")
                    #print("download " + illust.title)
                    ##print("caption")
                    #print(illust.caption.replace("<br />", "\n"))




                    if illust.type == "illust" or illust.type == "manga":
                        if illust.page_count == 1:
                            aapi.download(illust.meta_single_page.original_image_url, saving_direcory_path)
                        else:
                            for page in tqdm(illust.meta_pages, desc='illusts dowmload', leave=False):
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
                        
                        #mp4のオーバーフロー対策
                        if ugoira_delay in (3,6,7,9,11,12,13,14,15):
                            fps = round(fps,2)
                        
                        
                        #うごイラを保存するフォルダの作成
                        if not os.path.isdir(dir_name):
                            os.mkdir(dir_name)
                        
                        
                        #うごイラに使われているすべての画像のダウンロード(オリジナル) 
                        #高画質低速
                        for frame in tqdm(range(ugoira_frames), desc='ugoiras download', leave=False):
                            if os.path.exists(f'{dir_name}/{illust_id}_ugoira{frame}{ugoira_url[1]}'):
                                continue
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
                            
                            

                                
                                
                        #一つのファイルにまとめたhtml
                        if html_onefile == True:
                            import base64
                            illust_b64 = []
                            img_ext = frames[0].split('.')[-1]
                            for num, frame in enumerate(frames):
                                with open(frame, 'rb') as f:
                                    illust_b64.append([f'data:image/{img_ext};base64,{base64.b64encode(f.read()).decode()}', ugoira.ugoira_metadata.frames[num]['delay']])

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
                                        img.src = illust_b64[i][0];
                                        images.push([img, illust_b64[i][1]]);
                                    }}
                                    const canvas = document.querySelector('#ugoira');
                                    const context = canvas.getContext('2d');
                                    let count = 0;
                                    const drawImage = (index) => {{
                                        if(index>={frames}) index=0;
                                        context.clearRect(0, 0, canvas.width, canvas.height);
                                        context.drawImage(images[index][0], 0, 0);
                                        setTimeout(drawImage, images[index][1], index+1)
                                    }};
                                    window.addEventListener('load', () => drawImage(0));
                                </script>
                            </body>
                            </html>
                            """.format(width=width, height=height, frames=ugoira_frames, illust_id=illust_id, illust_b64=str(illust_b64))
                            with open(f'{saving_direcory_path}/{illust_id}.html', 'w', encoding='utf-8') as f:
                                f.write(html)

                            

                        
                        

                    #max_download_worksに達したら2重ループをやめる
                    #https://note.nkmk.me/python-break-nested-loops/
                    if download_work_no >= max_download_works:
                        finish_flag=True
                        break
                
                
                if finish_flag == True:
                   break
               
                next_qs = aapi.parse_qs(user_illusts.next_url)
                if next_qs == None:
                    break                    
                else:
                    sleep(1)
                    next_qs.update({"type":None})
                    user_illusts = aapi.user_illusts(**next_qs)
                       


            except:
                tqdm.write("error")
                #print("error")
                import traceback
                traceback.print_exc()
                sleep(60)
                break
                #continueだとuser_illustsを新たにとってこれずエラーて回るのでbreakで次のユーザーにまわしちゃう
                #continue
               
        
        tqdm.write("-----------------------------")
        tqdm.write("Download complete!　Thanks to {:<10}".format(user_id) + user_name)
        tqdm.write("")
        #print("-----------------------------")
        #print("Download complete!　Thanks to {:<10}".format(user_id) + user_name)
        #print()





