cd /d %~dp0
call C:\Users\ユーザー\Anaconda3\Scripts\activate.bat
call activate base

for %%i in (%*) do (
python %%i
)


pause
