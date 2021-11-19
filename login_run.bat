cd /d %~dp0
call G:\anaconda3\Scripts\activate.bat
call activate base

python pixiv_auth.py login



pause