import subprocess, time, sys, os, getpass
from pathlib import Path

# Checking if LINE is installed and installing the LINE APK if required
checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
if checkLineInstallationOutput == '':
    print("LINE is not installed. Installing LINE Now...")
    subprocess.run("adb install ~/Desktop/APKs/line-10-21-3.apk", shell=True)
    print("LINE installation finished")
else:
    print("LINE is already installed")

# Check if login is required
registrationRequired = True
subprocess.run("adb logcat -c", shell=True)
subprocess.run("adb shell am start -n jp.naver.line.android/.activity.SplashActivity", shell=True)
time.sleep(35)
checkLineRegistrationRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep jp.naver.line.android/com.linecorp.registration.ui.RegistrationActivity", shell=True, stdout=subprocess.PIPE)
checkLineRegistrationRequiredOutput = checkLineRegistrationRequired.stdout.read().decode("ascii")
if checkLineRegistrationRequiredOutput == '':
    verifyLineRegistrationNotRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep jp.naver.line.android/.activity.main.MainActivity", shell=True, stdout=subprocess.PIPE)
    verifyLineRegistrationNotRequiredOutput = verifyLineRegistrationNotRequired.stdout.read().decode("ascii")
    if verifyLineRegistrationNotRequiredOutput != '':
        registrationRequired = False
        print("LINE login not required")
    else:
        print("Error detected. Exiting the program")
        sys.exit()
else:
    registrationRequired = True
    print("LINE login required")

# LINE login
if registrationRequired == True:
    print("Logging in to LINE...")
    phoneNumber = input("Enter phone number: ")
    os.putenv("phoneNumber", phoneNumber)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartOne.sh")
    lineOtp = input("Enter LINE OTP: ")
    os.putenv("lineOtp", lineOtp)
    linePassword = getpass.getpass("Enter LINE Password: ")
    os.putenv("linePassword", linePassword)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartTwo.sh")
    time.sleep(25)
    print("LINE logged in")
    # Enter Chats
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 160")
    time.sleep(3)

# Open LINE's Keep Memo
print("Opening LINE's Keep Memo...")
os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineOpenKeepMemo.sh")
time.sleep(5)
print("LINE's Keep Memo Opened")

# Reading a text file of URLs and sending those URLs on LINE's Keep Memo
home = str(Path.home())
sendKeepMemoUrlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for lineUrl in sendKeepMemoUrlFile:
    os.putenv("url", lineUrl)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160")
    time.sleep(5)
    os.system("adb shell input keyevent 21 ; adb shell input keyevent 21")

sendKeepMemoUrlFile.close()

openWebviewUrlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
# Open the URLs using WebView in LINE
for lineUrl in openWebviewUrlFile:
    lineUrl = lineUrl.rstrip("\n")
    formattedLineUrl = lineUrl.replace(" ", "")
    formattedLineUrl = formattedLineUrl.replace("/", r"\/")
    print("Opening "+lineUrl+" using WebView on LINE...")
    adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' +formattedLineUrl+ '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebViewCommand)
    print("Opened "+lineUrl+" using WebView on LINE")
    time.sleep(45)
    isBackInKeepMemoChat = False
    while not isBackInKeepMemoChat:
        subprocess.Popen("adb logcat -c", shell=True)
        subprocess.Popen("adb shell input keyevent 4", shell=True)
        time.sleep(10)
        verifyInKeepMemoChat = subprocess.Popen("adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService", shell=True, stdout=subprocess.PIPE)
        verifyInKeepMemoChatOutput = verifyInKeepMemoChat.stdout.read().decode("ascii")
        if verifyInKeepMemoChatOutput != "":
            isBackInKeepMemoChat = True
            print("Closing the current WebView, opening the following URL...")
        else:
            isBackInKeepMemoChat = False

openWebviewUrlFile.close()