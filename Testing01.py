from pathlib import Path
import os, time, subprocess

# Open Text File of URLs and opening those URLs on WebView
home = str(Path.home())
urlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/URLs", "r")

for lineUrl in urlFile:
    lineUrl = lineUrl.rstrip("\n")
    lineUrl = lineUrl.replace(" ", "")
    lineUrl = lineUrl.replace('/', r'\/')
    adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' +lineUrl+ '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebViewCommand)
    time.sleep(45)
    isBackInKeepMemo = False
    while not isBackInKeepMemo:
        subprocess.Popen("adb logcat -c", shell=True)
        subprocess.Popen("adb shell input keyevent 4", shell=True)
        time.sleep(10)
        verifyInKeepMemo = subprocess.Popen("adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService", shell=True, stdout=subprocess.PIPE)
        verifyInKeepMemoOutput = verifyInKeepMemo.stdout.read().decode("ascii")
        if verifyInKeepMemoOutput != "":
            isBackInKeepMemo = True
        else:
            isBackInKeepMemo = False
