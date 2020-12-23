from pathlib import Path
import os, time, subprocess

# Open Text File of URLs and sending them on LINE
home = str(Path.home())
urlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/URLs", "r")
for url in urlFile:
    os.putenv("url", url)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160")
    time.sleep(5)
    os.system("adb shell input keyevent 21 ; adb shell input keyevent 21")

urlFile.close()




