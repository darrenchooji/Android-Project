import subprocess, time, os
from pathlib import Path

# Check if Android Webview crashed
def android_webview_anomaly_checking():
    adb_verify_webview_crash_command = r'''adb logcat -d ActivityManager:I *:S | grep "Scheduling restart of crashed service" | grep org.chromium.content.app.SandboxedProcessService'''
    verify_webview_crash = subprocess.Popen(adb_verify_webview_crash_command, shell=True, stdout=subprocess.PIPE)
    verify_webview_crash_output = verify_webview_crash.stdout().read().decode("ascii")
    if verify_webview_crash_output != '':
        return True
    else:
        return False

# Check if Chrome's Custom Tab Activity crashed
def chrome_custom_tab_activity_anomaly_checking():
    subprocess.run(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramWebview.xml''', shell=True)
    adb_verify_webview_crash_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aw, Snap!"[^>]*resource-id="com.android.chrome:id\/sad_tab_title"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramWebview.xml) ; echo $coords'''
    verify_webview_crash = subprocess.Popen(adb_verify_webview_crash_command, shell=True, stdout=subprocess.PIPE)
    time.sleep(3)
    verify_webview_crash_output = verify_webview_crash.stdout.read().decode("ascii")
    verify_webview_crash_output = verify_webview_crash_output.rstrip("\n")
    if verify_webview_crash_output != '':
        return True
    else:
        return False

def line(website):
    # Checking if installation of Link APK is required
    check_line_installation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
    check_line_installation_output = check_line_installation.stdout.read().decode("ascii")
    if check_line_installation_output == '':
        print("LINE is not installed. Installing LINE now...")
        subprocess.run("adb install ~/Desktop/APKs/line*.apk", shell=True)
        print("LINE installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n jp.naver.line.android/.activity.SplashActivity", shell=True)
    time.sleep(10)
    check_line_registration_required = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep jp.naver.line.android/com.linecorp.registration.ui.RegistrationActivity", shell=True, stdout=subprocess.PIPE)
    check_line_registration_required_output = check_line_registration_required.stdout.read().decode("ascii")
    if check_line_registration_required_output == '':
        registration_required = False
    else:
        registration_required = True
        print("LINE login required")

    # Line login
    if registration_required == True:
        home_path = str(Path.home())
        line_credentials = open(home_path+"/Desktop/Credentials/Line.txt", "r")
        for credentials in line_credentials:
            credentials_list = credentials.split(";")
            phone_number = credentials_list[0]
            password = credentials_list[1]
        print("Logging in to LINE...")
        os.putenv("phone_number", phone_number)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartOne.sh")
        line_otp = input("Enter LINE OTP: ")
        os.putenv("line_otp", line_otp)
        os.putenv("line_password", password)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineRegistrationPartTwo.sh")
        time.sleep(40)
        print("LINE logged in")

        line_credentials.close()

        # Enter Chats
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
        time.sleep(3)

    # Open LINE's Keep Memo
    print("Opening LINE's Keep Memo...")
    os.system("cd ~/Desktop/AndroidAnomalyDetection/LineShellScripts ; ./LineOpenKeepMemo.sh")
    time.sleep(5)
    print("LINE's Keep Memo Opened")

    # Sending URL to LINE's Keep Memo and opening that particular URL using LINE's WebView
    os.system("adb logcat -c")
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    website = website.rstrip("\n")
    formatted_line_url = website.replace("/", r"\/")
    print("Opening "+website+" using WebView on LINE...")
    adb_open_url_in_webview_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formatted_line_url + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
    subprocess.Popen(adb_open_url_in_webview_command, shell=True)
    print("Opened "+website+" using WebView on LINE")
    time.sleep(45)

    anomaly = android_webview_anomaly_checking()

    if not anomaly:
        # Exiting Line's WebView
        print("No anomaly detected for "+website)
        is_back_in_keep_memo_chat = False
        while not is_back_in_keep_memo_chat:
            subprocess.Popen("adb logcat -c", shell=True)
            subprocess.Popen("adb shell input keyevent 4", shell=True)
            time.sleep(10)
            verify_in_keep_memo_chat = subprocess.Popen(
                "adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService",
                shell=True, stdout=subprocess.PIPE)
            verify_in_keep_memo_chat_output = verify_in_keep_memo_chat.stdout.read().decode("ascii")
            if verify_in_keep_memo_chat_output != "":
                is_back_in_keep_memo_chat = True
            else:
                is_back_in_keep_memo_chat = False
    else:
        print("Anomaly detected for "+website)

def telegram(website):
    # Checking if installation of Telegram APK is required
    check_telegram_installation = subprocess.Popen("adb shell pm list packages | grep org.telegram.messenger", shell=True, stdout=subprocess.PIPE)
    check_telegram_installation_output = check_telegram_installation.stdout.read().decode("ascii")
    if check_telegram_installation_output == '':
        print("Telegram is not installed. Installing Telegram Now...")
        subprocess.run("adb install ~/Desktop/APKs/telegram*.apk", shell=True)
        print("Telegram installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity", shell=True)
    time.sleep(15)
    check_telegram_registration_required = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep org.telegram.messenger/org.telegram.ui.IntroActivity | grep Displayed", shell=True, stdout=subprocess.PIPE)
    check_telegram_registration_required_output = check_telegram_registration_required.stdout.read().decode("ascii")
    if check_telegram_registration_required_output == '':
        registration_required = False
    else:
        registration_required = True
        print("Telegram login required")

    # Telegram login
    if registration_required == True:
        home_path = str(Path.home())
        telegram_credentials = open(home_path+"/Desktop/Credentials/Telegram.txt", "r")
        for credentials in telegram_credentials:
            credentials_list = credentials.split(";")
            phone_number = credentials_list[0]
        os.putenv("phoneNumber", phone_number)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartOne.sh")
        telegram_otp = input("Enter Telegram OTP: ")
        os.putenv("telegramOtp", telegram_otp)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartTwo.sh")
        print("Login to Telegram finished")
        telegram_credentials.close()

    # Open Telegram's Saved Messages
    adb_open_telegram_navigation_menu_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramChatsPage.xml ; navMenu=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Open navigation menu"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramChatsPage.xml) ; adb shell input tap $navMenu'''
    subprocess.Popen(adb_open_telegram_navigation_menu_command, shell=True)
    time.sleep(5)
    adb_open_telegram_saved_messages_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramNavMenuPage.xml ; savedMessages=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Saved Messages"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramNavMenuPage.xml) ; adb shell input tap $savedMessages'''
    subprocess.Popen(adb_open_telegram_saved_messages_command, shell=True)
    print("Opened Telegram's Saved Messages")
    time.sleep(3)

    # Sending URL to Telegram's Saved Messages and opening that particular URL using Telegram's Chrome Custom Tab Activity
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(3)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    subprocess.run("adb logcat -c", shell=True)
    time.sleep(3)
    website = website.rstrip("\n")
    formatted_telegram_url = website.replace("/", r"\/")
    print("Opening "+website+" using WebView on Telegram...")
    adb_open_url_in_webview_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramSavedMessages.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formatted_telegram_url + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramSavedMessages.xml) ; adb shell input tap $url'''
    os.system(adb_open_url_in_webview_command)
    time.sleep(10)
    verify_chrome_first_activity = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep Displayed | grep com.android.chrome/org.chromium.chrome.browser.firstrun.FirstRunActivity", shell=True, stdout=subprocess.PIPE)
    verify_chrome_first_activity_output = verify_chrome_first_activity.stdout.read().decode("ascii")
    if verify_chrome_first_activity_output != '':
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
        time.sleep(3)
        os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
        print("Opened "+website+" using WebView on Telegram")
        time.sleep(10)
    else:
        time.sleep(5)

    anomaly = chrome_custom_tab_activity_anomaly_checking()
    if not anomaly:
        print("No anomaly detected for "+website)
    else:
        print("Anomaly detected for "+website)

    # Exiting Telegram's Chrome Custom Tab Activity
    time.sleep(10)
    adb_close_web_view_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramWebview.xml ; closeWebview=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close tab"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramWebview.xml) ; adb shell input tap $closeWebview'''
    subprocess.Popen(adb_close_web_view_command, shell=True)

def facebookmessenger(website):
    # Checking if installation of Facebook Messenger is required
    check_facebook_messenger_installation = subprocess.Popen("adb shell pm list packages | grep com.facebook.orca",
                                                          shell=True, stdout=subprocess.PIPE)
    check_facebook_messenger_installation_output = check_facebook_messenger_installation.stdout.read().decode("ascii")
    if check_facebook_messenger_installation_output == '':
        print("Facebook Messenger is not installed. Installing Facebook Messenger now...")
        subprocess.run("adb install ~/Desktop/APKs/messenger*.apk", shell=True)
        print("Facebook Messenger installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity", shell=True)
    time.sleep(10)
    check_facebook_messenger_registration_required = subprocess.Popen(
        "adb logcat -d ActivityTaskManager:I *:S | grep com.facebook.orca/com.facebook.messaging.accountlogin.AccountLoginActivity",
        shell=True, stdout=subprocess.PIPE)
    check_facebook_messenger_registration_required_output = check_facebook_messenger_registration_required.stdout.read().decode(
        "ascii")
    if check_facebook_messenger_registration_required_output != '':
        registration_required = True
        print("Facebook Messenger login required")
    else:
        registration_required = False

    home_path = str(Path.home())
    facebook_messenger_credentials = open(home_path + "/Desktop/Credentials/FacebookMessenger.txt", "r")
    for credentials in facebook_messenger_credentials:
        credentials_list = credentials.split(";")
        email = credentials_list[0]
        password = credentials_list[1]
        username = credentials_list[2]

    # Facebook Messenger login
    if registration_required == True:
        print("Logging in to Facebook Messenger...")
        os.putenv("email", email)
        os.putenv("password", password)
        os.system("cd ~/Desktop/AndroidAnomalyDetection/FacebookMessengerShellScripts ; ./FacebookMessengerRegistration.sh")

    facebook_messenger_credentials.close()

    # Open Facebook Messenger's Self-Messaging
    os.system("adb shell svc wifi disable")
    time.sleep(3)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(5)
    os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/RecentApps.xml ; closeRecentApps=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Close all"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/RecentApps.xml) ; adb shell input tap $closeRecentApps''')
    time.sleep(5)
    os.system("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity")
    time.sleep(15)
    os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerChats.xml ; newMessage=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="New message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerChats.xml) ; adb shell input tap $newMessage''')
    time.sleep(5)
    username = username.replace(" ", "%s")
    os.putenv("username", username)
    os.system("adb shell input text $username")
    time.sleep(5)
    os.system("adb shell svc wifi enable")
    time.sleep(10)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(7)

    # Sending URL to own profile and opening that particular URL using Facebook Messenger's Webview
    os.system(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelfMessage.xml ; msg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aa"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelfMessage.xml) ; adb shell input tap $msg''')
    time.sleep(3)
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(3)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    website = website.rstrip("\n")
    formatted_messenger_url = website.replace("/", "\/")
    print("Opening " + website + " using WebView on Facebook Messenger...")
    adb_open_url_in_webview_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerOwnProfile.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formatted_messenger_url + '''"[^>]*content-desc=""[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerOwnProfile.xml) ; adb shell input tap $url'''
    os.system(adb_open_url_in_webview_command)
    print("Opened " + website + " using WebView on Facebook Messenger")
    time.sleep(45)

    anomaly = android_webview_anomaly_checking()
    time.sleep(10)

    if not anomaly:
        # Exiting Facebook Messenger's Webview
        print("No anomaly detected for "+website)
        adb_close_web_view_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerWebView.xml ; closeBrowser=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close browser"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerWebView.xml) ; adb shell input tap $closeBrowser'''
        os.system(adb_close_web_view_command)
    else:
        print("Anomaly detected for "+website)

# Reading file which contains the desired IM's package name and URL
home_path = str(Path.home())
url_file = open(home_path+"/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for urls in url_file:
    url_list = urls.split(";")
    im = url_list[0]
    website = url_list[1]
    if im == "jp.naver.line.android":
        line(website)
    elif im == "org.telegram.messenger":
        telegram(website)
    elif im == "com.facebook.orca":
        facebookmessenger(website)
    time.sleep(5)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(3)
    os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/RecentApps.xml ; closeRecentApps=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Close all"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/RecentApps.xml) ; adb shell input tap $closeRecentApps''')
    time.sleep(5)

url_file.close()
