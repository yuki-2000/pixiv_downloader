cd /d %~dp0
call G:\anaconda3\Scripts\activate.bat
call activate base

for %%i in (%*) do (
python %%i
)


pause