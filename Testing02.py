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

# Opening those URLs on WebView
for url in urlFile:
    formattedUrl=url.replace("/", r"\/")
    adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="'''+formattedUrl+'''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebViewCommand)
    time.sleep(50)
    isBackInKeepMemo = False
    while not isBackInKeepMemo:
        subprocess.Popen("adb logcat -c", shell=True)
        subprocess.Popen("adb shell input keyevent 4", shell=True)
        time.sleep(15)
        verifyInKeepMemo = subprocess.Popen("adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService", shell=True, stdout=subprocess.PIPE)
        verifyInKeepMemoOutput = verifyInKeepMemo.stdout.read().decode("ascii")
        if verifyInKeepMemoOutput != "":
            isBackInKeepMemo = True
        else:
            isBackInKeepMemo = False