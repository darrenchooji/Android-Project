import subprocess, time, os
from pathlib import Path

def line(website):
    checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
    checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
    if checkLineInstallationOutput == '':
        print("LINE is not installed. Installing LINE now...")
        subprocess.run("adb install ~/Desktop/APKs/line*.apk", shell=True)
        print("LINE installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n jp.naver.line.android/.activity.SplashActivity", shell=True)
    time.sleep(35)
    checkLineRegistrationRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep jp.naver.line.android/com.linecorp.registration.ui.RegistrationActivity", shell=True, stdout=subprocess.PIPE)
    checkLineRegistrationRequiredOutput = checkLineRegistrationRequired.stdout.read().decode("ascii")
    if checkLineRegistrationRequiredOutput == '':
        registrationRequired = False
    else:
        registrationRequired = True
        print("LINE login required")

    if registrationRequired == True:
        homePath = str(Path.home())
        lineCredentials = open(homePath+"/Desktop/Credentials/Line.txt", "r")
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

        lineCredentials.close()

        # Enter Chats
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
        time.sleep(3)

    # Open LINE's Keep Memo
    print("Opening LINE's Keep Memo...")
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineOpenKeepMemo.sh")
    time.sleep(5)
    print("LINE's Keep Memo Opened")

    # Sending URL to LINE's Keep Memo and opening that URL using LINE's WebView
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    os.system("adb shell input keyevent 4")
    time.sleep(3)
    website = website.rstrip("\n")
    formattedLineUrl = website.replace("/", r"\/")
    print("Opening "+website+" using WebView on LINE...")
    adbOpenUrlInWebviewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formattedLineUrl + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebviewCommand)
    print("Opened "+website+" using WebView on LINE")
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

def telegram(website):
    # Checking if Telegram is installed and installing the Telegram APK if required
    checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep org.telegram.messenger", shell=True, stdout=subprocess.PIPE)
    checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
    if checkLineInstallationOutput == '':
        print("Telegram is not installed. Installing Telegram Now...")
        subprocess.run("adb install ~/Desktop/APKs/telegram*.apk", shell=True)
        print("Telegram installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity", shell=True)
    time.sleep(35)
    checkLineRegistrationRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep org.telegram.messenger/org.telegram.ui.IntroActivity | grep Displayed", shell=True, stdout=subprocess.PIPE)
    checkLineRegistrationRequiredOutput = checkLineRegistrationRequired.stdout.read().decode("ascii")
    if checkLineRegistrationRequiredOutput == '':
        registrationRequired = False
    else:
        registrationRequired = True
        print("Telegram login required")

    # Telegram login
    if registrationRequired == True:
        homePath = str(Path.home())
        telegramCredentials = open(homePath+"/Desktop/Credentials/Telegram.txt", "r")
        for credentials in telegramCredentials:
            credentialsList = credentials.split(";")
            phoneNumber = credentialsList[0]
        os.putenv("phoneNumber", phoneNumber)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartOne.sh")
        telegramOtp = input("Enter Telegram OTP: ")
        os.putenv("telegramOtp", telegramOtp)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartTwo.sh")
        print("Login to Telegram finished")
        telegramCredentials.close()

    # Open Telegram's Saved Messages
    adbOpenTelegramNavigationMenuCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramChatsPage.xml ; navMenu=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Open navigation menu"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramChatsPage.xml) ; adb shell input tap $navMenu'''
    subprocess.Popen(adbOpenTelegramNavigationMenuCommand, shell=True)
    time.sleep(5)
    adbOpenTelegramSavedMessagesCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramNavMenuPage.xml ; savedMessages=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Saved Messages"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramNavMenuPage.xml) ; adb shell input tap $savedMessages'''
    subprocess.Popen(adbOpenTelegramSavedMessagesCommand, shell=True)
    print("Opened Telegram's Saved Messages")
    time.sleep(15)
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(10)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    os.system("adb shell input keyevent 4")
    time.sleep(3)
    website = website.rstrip("\n")
    formattedTelegramUrl = website.replace("/", r"\/")
    print("Opening "+website+" using WebView on Telegram...")
    adbOpenUrlInWebviewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramSavedMessages.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formattedTelegramUrl + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramSavedMessages.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebviewCommand)
    time.sleep(20)
    subprocess.run("adb logcat -c", shell=True)
    verifyChromeFirstActivity = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep Displayed | grep com.android.chrome/org.chromium.chrome.browser.firstrun.FirstRunActivity", shell=True, stdout=subprocess.PIPE)
    if verifyChromeFirstActivity != '':
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
        time.sleep(5)
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
        print("Opened "+website+" using WebView on Telegram")
        time.sleep(45)
    else:
        time.sleep(25)
    adbCloseWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramWebview.xml ; closeWebview=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close tab"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramWebview.xml) ; adb shell input tap $closeWebview'''
    os.system(adbCloseWebViewCommand)
    time.sleep(15)


def facebookMessenger(website):
    # Checking if Facebook Messenger is installed and installing the APK if required
    checkFacebookMessengerInstallation = subprocess.Popen("adb shell pm list packages | grep com.facebook.orca",
                                                          shell=True, stdout=subprocess.PIPE)
    checkFacebookMessengerInstallationOutput = checkFacebookMessengerInstallation.stdout.read().decode("ascii")
    if checkFacebookMessengerInstallationOutput == '':
        print("Facebook Messenger is not installed. Installing Facebook Messenger now...")
        subprocess.run("adb install ~/Desktop/APKs/messenger*.apk", shell=True)
        print("Facebook Messenger installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity", shell=True)
    time.sleep(30)
    checkFacebookMessengerRegistrationRequired = subprocess.Popen(
        "adb logcat -d ActivityTaskManager:I *:S | grep com.facebook.orca/com.facebook.messaging.accountlogin.AccountLoginActivity",
        shell=True, stdout=subprocess.PIPE)
    checkFacebookMessengerRegistrationRequiredOutput = checkFacebookMessengerRegistrationRequired.stdout.read().decode(
        "ascii")
    if checkFacebookMessengerRegistrationRequiredOutput != '':
        registrationRequired = True
        print("Facebook Messenger login required")
    else:
        registrationRequired = False

    homePath = str(Path.home())
    facebookMessengerCredentials = open(homePath + "/Desktop/Credentials/FacebookMessenger.txt", "r")
    for credentials in facebookMessengerCredentials:
        credentialsList = credentials.split(";")
        email = credentialsList[0]
        password = credentialsList[1]
        username = credentialsList[2]

    if registrationRequired == True:
        print("Logging in to Facebook Messenger...")
        os.putenv("email", email)
        os.putenv("password", password)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/FacebookMessengerShellScripts ; ./FacebookMessengerRegistration.sh")

    facebookMessengerCredentials.close()
    time.sleep(10)

    # Open Facebook Messenger's Self-Messaging
    os.system("adb shell svc wifi disable")
    time.sleep(3)
    os.system("adb shell svc data disable")
    time.sleep(3)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(15)
    os.system("adb shell input keyevent 20 ; adb shell input keyevent DEL")
    time.sleep(15)
    os.system("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity")
    time.sleep(30)
    os.system(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerChats.xml ; newMessage=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="New Message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerChats.xml) ; adb shell input tap $newMessage''')
    time.sleep(10)
    os.system("adb shell svc wifi enable")
    time.sleep(3)
    os.system("adb shell svc data enable")
    time.sleep(30)
    username = username.replace(" ", "%s")
    os.putenv("username", username)
    os.system("adb shell input text $username")
    time.sleep(30)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(25)

    # Sending URL to own profile and opening that URL using WebView in Facebook Messenger
    os.system(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelfMessage.xml ; msg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aa"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelfMessage.xml) ; adb shell input tap $msg''')
    time.sleep(5)
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(10)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(5)
    os.system("adb shell input keyevent 4")
    time.sleep(5)
    website = website.rstrip("\n")
    formattedMessengerUrl = website.replace("/", "\/")
    print("Opening " + website + " using WebView on Facebook Messenger...")
    adbOpenUrlInWebviewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerOwnProfile.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formattedMessengerUrl + '''"[^>]*content-desc=""[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerOwnProfile.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebviewCommand)
    print("Opened " + website + " using WebView on Facebook Messenger")
    time.sleep(45)
    adbCloseWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerWebView.xml ; closeBrowser=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close browser"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerWebView.xml) ; adb shell input tap $closeBrowser'''
    os.system(adbCloseWebViewCommand)
    time.sleep(20)

homePath = str(Path.home())
urlFile = open(homePath+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for urls in urlFile:
    urlList = urls.split(";")
    im = urlList[0]
    website = urlList[1]
    if im == "jp.naver.line.android":
        line(website)
    elif im == "org.telegram.messenger":
        telegram(website)
    elif im == "com.facebook.orca":
        facebookMessenger(website)
    time.sleep(5)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(15)
    os.system("adb shell input keyevent 20 ; adb shell input keyevent DEL")

urlFile.close()
