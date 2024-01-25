@echo off
echo Compiling Python script to executable...

REM Adding audio files and config.ini along with words.txt
pyinstaller --onefile --noconsole --add-data "words.txt;." --add-data "time1.wav;." --add-data "time2.wav;." --add-data "time3.wav;." --add-data "time4.wav;." --add-data "config.ini;." WordMaster.py

echo Removing temporary files...
rmdir /s /q build
del /f /q WordMaster.spec

echo Creating a zip file with the executable, words.txt, and other essential files...
powershell Compress-Archive -Path dist\WordMaster.exe, words.txt, time1.wav, time2.wav, time3.wav, time4.wav, config.ini -DestinationPath WordMaster.zip -Force

echo Removing distribution files...
rmdir /s /q dist

echo Compilation and packaging finished.