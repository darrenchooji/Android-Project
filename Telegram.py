import subprocess, time, sys, os
from pathlib import Path

# Checking if Telegram is installed and installing the Telegram APK if required
checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep org.telegram.messenger", shell=True, stdout=subprocess.PIPE)
checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
if checkLineInstallationOutput == '':
    print("Telegram is not installed. Installing Telegram Now...")
    subprocess.run("adb install ~/Desktop/APKs/telegram*.apk", shell=True)
    print("Telegram installation finished")
else:
    print("Telegram is already installed")

# Check if login is required
registrationRequired = True
subprocess.run("adb logcat -c", shell=True)
subprocess.run("adb shell am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity", shell=True)
time.sleep(35)
checkLineRegistrationRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep org.telegram.messenger/org.telegram.ui.IntroActivity | grep Displayed", shell=True, stdout=subprocess.PIPE)
checkLineRegistrationRequiredOutput = checkLineRegistrationRequired.stdout.read().decode("ascii")
if checkLineRegistrationRequiredOutput == '':
    verifyLineRegistrationNotRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep org.telegram.messenger/org.telegram.ui.LaunchActivity | grep Displayed", shell=True, stdout=subprocess.PIPE)
    verifyLineRegistrationNotRequiredOutput = verifyLineRegistrationNotRequired.stdout.read().decode("ascii")
    if verifyLineRegistrationNotRequiredOutput != '':
        registrationRequired = False
        print("Telegram login not required")
    else:
        print("Error detected. Exiting the program")
        sys.exit()
else:
    registrationRequired = True
    print("Telegram login required")

# Telegram login
if registrationRequired == True:
    print("Logging in to Telegram...")
    phoneNumber = input("Enter phone number: ")
    os.putenv("phoneNumber", phoneNumber)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartOne.sh")
    telegramOtp = input("Enter Telegram OTP: ")
    os.putenv("telegramOtp", telegramOtp)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartTwo.sh")
    print("Login to Telegram finished")

# Open Telegram's Saved Messages
adbOpenTelegramNavigationMenuCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramChatsPage.xml ; navMenu=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Open navigation menu"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramChatsPage.xml) ; adb shell input tap $navMenu'''
subprocess.Popen(adbOpenTelegramNavigationMenuCommand, shell=True)
time.sleep(5)
adbOpenTelegramSavedMessagesCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramNavMenuPage.xml ; savedMessages=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Saved Messages"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramNavMenuPage.xml) ; adb shell input tap $savedMessages'''
subprocess.Popen(adbOpenTelegramSavedMessagesCommand, shell=True)
print("Opened Telegram's Saved Messages")

time.sleep(15)

# Reading a text file of URLs and sending those URLs on Telegram's Saved Messages
home = str(Path.home())
sendSavedMessagesUrlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for telegramUrl in sendSavedMessagesUrlFile:
    os.putenv("url", telegramUrl)
    os.system("adb shell input text $url")
    time.sleep(10)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(5)
    os.system("adb shell input keyevent 21 ; adb shell input keyevent 21")

sendSavedMessagesUrlFile.close()

index = 0
openWebviewUrlFile = open(home+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for telegramUrl in openWebviewUrlFile:
    telegramUrl = telegramUrl.rstrip("\n")
    formattedTelegramUrl = telegramUrl.replace(" ", "")
    formattedTelegramUrl = telegramUrl.replace("/", r"\/")
    print("Opening "+telegramUrl+" using WebView on Telegram...")
    adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramSavedMessages.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="'''+formattedTelegramUrl+'''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramSavedMessages.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebViewCommand)
    # Checking if it is Chrome's First Run
    if index==0:
        time.sleep(25)
        verifyChromeFirstActivity = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep Displayed | grep com.android.chrome/org.chromium.chrome.browser.firstrun.FirstRunActivity", shell=True, stdout=subprocess.PIPE)
        verifyChromeFirstActivityOutput = verifyChromeFirstActivity.stdout.read().decode("ascii")
        if verifyChromeFirstActivityOutput != '':
                os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
                time.sleep(5)
                os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    print("Opened "+telegramUrl+" using WebView on Telegram")
    time.sleep(45)
    adbCloseWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramWebview.xml ; closeWebview=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close tab"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramWebview.xml) ; adb shell input tap $closeWebview'''
    os.system(adbCloseWebViewCommand)
    time.sleep(15)
    index+=1
   
openWebviewUrlFile.close()
