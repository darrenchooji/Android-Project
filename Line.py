import subprocess, time, sys, os, getpass
from pathlib import Path

# Checking if LINE is installed and installing the LINE APK if required
checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
if checkLineInstallationOutput == '':
    print("LINE is not installed. Installing LINE Now...")
    subprocess.run("adb install ~/Desktop/APKs/line*.apk", shell=True)
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
    home = str(Path.home())
    lineCredentials = open(home + "/Desktop/Credentials/Line.txt", "r")
    for credentials in lineCredentials:
        credentialsList = credentials.split(";")
        phoneNumber = credentialsList[0]
        password = credentialsList[1]
    print("Logging in to LINE...")
    os.putenv("phoneNumber", phoneNumber)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartOne.sh")
    lineOtp = input("Enter LINE OTP: ")
    os.putenv("lineOtp", lineOtp)
    os.putenv("linePassword", password)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartTwo.sh")
    time.sleep(40)
    print("LINE logged in")
    # Enter Chats
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)

# Open LINE's Keep Memo
print("Opening LINE's Keep Memo...")
os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineOpenKeepMemo.sh")
time.sleep(5)
print("LINE's Keep Memo Opened")

# Reading a text file of URLs and sending those URLs to own profile and open those URLs using WebView on LINE
currentWorkingDirectory = os.getcwd()
urlFile = open(currentWorkingDirectory+"/URLs/urls.txt", "r")
for lineUrl in urlFile:
    os.putenv("url", lineUrl)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    os.system("adb shell input keyevent 4")
    time.sleep(3)
    lineUrl = lineUrl.rstrip("\n")
    formattedLineUrl = lineUrl.replace("/", r"\/")
    print("Opening " + lineUrl + " using WebView on LINE...")
    adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formattedLineUrl + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebViewCommand)
    print("Opened " + lineUrl + " using WebView on LINE")
    time.sleep(45)
    isBackInKeepMemoChat = False
    while not isBackInKeepMemoChat:
        subprocess.Popen("adb logcat -c", shell=True)
        subprocess.Popen("adb shell input keyevent 4", shell=True)
        time.sleep(10)
        verifyInKeepMemoChat = subprocess.Popen(
            "adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService",
            shell=True, stdout=subprocess.PIPE)
        verifyInKeepMemoChatOutput = verifyInKeepMemoChat.stdout.read().decode("ascii")
        if verifyInKeepMemoChatOutput != "":
            isBackInKeepMemoChat = True
        else:
            isBackInKeepMemoChat = False
    os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/LineKeepMemo.xml ; editmsg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /class="android.widget.EditText"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/LineKeepMemo.xml) ; adb shell input tap $editmsg''')
    time.sleep(5)

urlFile.close()