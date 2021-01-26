import os
import subprocess
import time
import random
from pathlib import Path


home_path = str(Path.home())
serial_number = random.randint(0000, 9999)
log_file = open(home_path + "/Desktop/AndroidAnomalyDetection/anomalydetectionlog" + str(serial_number) + ".txt", "w")


# Check if webpage downloaded any files/folders
def webpage_downloaded_file_checking():
    subprocess.Popen("adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/CheckingPage.xml",
                     shell=True)
    adb_verify_check_file_existence_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Do you want to download [a-zA-Z\|\/\*\~\`\^\!\-_,.? ]*"[^>]*resource-id="com.android.chrome:id\/infobar_message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/CheckingPage.xml) ; echo $coords'''
    verify_file_existence = subprocess.Popen(adb_verify_check_file_existence_command, shell=True,
                                             stdout=subprocess.PIPE)
    verify_file_existence_output = verify_file_existence.stdout.read().decode("ascii")
    verify_file_existence_output = verify_file_existence_output.rstrip("\n")
    if verify_file_existence_output != '':
        log_file.write("Anomaly detected! Webpage attempted to download a file that already exists in the phone!\n")
        return True
    else:
        adb_verify_webview_download_command = r'''adb logcat -d MediaProvider:D *:S | grep /storage/emulated/0/Download/'''
        verify_webview_download = subprocess.Popen(adb_verify_webview_download_command, shell=True,
                                                   stdout=subprocess.PIPE)
        verify_webview_download_output = verify_webview_download.stdout.read().decode("ascii")
        if verify_webview_download_output != '':
            log_file.write("Anomaly detected! Webpage has downloaded a file!\n")
            return True
        else:
            return False


# Check if webpage crashed
def webview_crash_checking():
    adb_verify_webview_crash_command = r'''adb logcat -d ActivityManager:I *:S | grep "Scheduling restart of crashed service" | grep org.chromium.content.app.SandboxedProcessService'''
    verify_webview_crash = subprocess.Popen(adb_verify_webview_crash_command, shell=True, stdout=subprocess.PIPE)
    verify_webview_crash_output = verify_webview_crash.stdout.read().decode("ascii")
    if verify_webview_crash_output != '':
        log_file.write("Anomaly detected! Webpage crashed!\n")
        return True
    else:
        return False


# Checking for anomalies in Android WebView
def android_webview_anomaly_checking(verification_text):
    # Check if webpage crashed
    crash = webview_crash_checking()
    if crash:
        return 1
    else:
        # Call function to check if webpage has downloaded any file/folder
        download = webpage_downloaded_file_checking()
        if download:
            return 2
        else:
            # Check if webpage contains the verification text
            subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Webview.xml''',
                             shell=True)
            verification_text = verification_text.replace("|", "\|")
            verification_text = verification_text.replace("/", "\/")
            verification_text = verification_text.rstrip("\n")
            adb_verify_webview_crash_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="[a-zA-Z\|\/\*\~\`\^\!\-,. ]*''' + verification_text + '''[a-zA-Z\|\/\*\~\`\^\!\-,. ]*"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Webview.xml) ; echo $coords'''
            verify = subprocess.Popen(adb_verify_webview_crash_command, shell=True, stdout=subprocess.PIPE)
            verify_output = verify.stdout.read().decode("ascii")
            verify_output = verify_output.rstrip("\n")
            if verify_output == '':
                return 3
            else:
                log_file.write("No anomaly detected\n")
                return 4


def line(website, verification_text):
    # Checking if installation of Link APK is required
    check_line_installation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True,
                                               stdout=subprocess.PIPE)
    check_line_installation_output = check_line_installation.stdout.read().decode("ascii")
    if check_line_installation_output == '':
        print("LINE is not installed. Installing LINE now...")
        subprocess.run("adb install ~/Desktop/APKs/line*.apk", shell=True)
        print("LINE installation finished")

    # Check if login is required
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n jp.naver.line.android/.activity.SplashActivity", shell=True)
    time.sleep(10)
    check_line_registration_required = subprocess.Popen(
        "adb logcat -d ActivityTaskManager:I *:S | grep jp.naver.line.android/com.linecorp.registration.ui.RegistrationActivity",
        shell=True, stdout=subprocess.PIPE)
    check_line_registration_required_output = check_line_registration_required.stdout.read().decode("ascii")
    if check_line_registration_required_output == '':
        registration_required = False
    else:
        registration_required = True
        print("LINE login required")

    # Line login
    if registration_required:
        line_credentials = open(home_path + "/Desktop/Credentials/Line.txt", "r")
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
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(5)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    website = website.rstrip("\n")
    formatted_line_url = website.replace("/", r"\/")

    for x in range(3):
        log_file.write("Testing " + website.rstrip("\n") + " on Telegram (" + str(x + 1) + "/3)\n")
        os.system("adb logcat -c")
        adb_open_url_in_webview_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formatted_line_url + '''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
        subprocess.Popen(adb_open_url_in_webview_command, shell=True)
        time_countdown = 30.0
        while time_countdown > 0:
            start = time.time()
            result = android_webview_anomaly_checking(verification_text)
            end = time.time()
            if result == 3:
                elapsed_time = end - start
                time_countdown = time_countdown - elapsed_time
            else:
                break

        time.sleep(5)
        if result != 1:
            if result == 3:
                log_file.write("Anomaly detected! Webpage was loaded but did not contain the verification text!\n")

            # Exiting Line's WebView
            is_back_in_keep_memo_chat = False
            while not is_back_in_keep_memo_chat:
                subprocess.Popen("adb logcat -c", shell=True)
                subprocess.Popen("adb shell input keyevent 4", shell=True)
                time.sleep(5)
                verify_in_keep_memo_chat = subprocess.Popen(
                    "adb logcat -d ActivityManager:I *:S | grep Killing | grep com.google.android.webview:sandboxed_process0:org.chromium.content.app.SandboxedProcessService",
                    shell=True, stdout=subprocess.PIPE)
                verify_in_keep_memo_chat_output = verify_in_keep_memo_chat.stdout.read().decode("ascii")
                if verify_in_keep_memo_chat_output != "":
                    is_back_in_keep_memo_chat = True
                else:
                    is_back_in_keep_memo_chat = False
        elif result == 1:
            time_counter = 30.0 - time_countdown
            log_file.write("Detected at "+str(time_counter)+" seconds\n")


def facebookmessenger(website, verification_text):
    # Checking if installation of Facebook Messenger is required
    check_facebook_messenger_installation = subprocess.Popen("adb shell pm list packages | grep com.facebook.orca",
                                                             shell=True, stdout=subprocess.PIPE)
    check_facebook_messenger_installation_output = check_facebook_messenger_installation.stdout.read().decode("ascii")
    if check_facebook_messenger_installation_output == '':
        print("Facebook Messenger is not installed. Installing Facebook Messenger now...")
        subprocess.run("adb install ~/Desktop/APKs/messenger*.apk", shell=True)
        print("Facebook Messenger installation finished")

    subprocess.run("adb shell svc wifi disable", shell=True)
    time.sleep(3)
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity", shell=True)
    time.sleep(10)

    # Check if login is required
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

    facebook_messenger_credentials = open(home_path + "/Desktop/Credentials/FacebookMessenger.txt", "r")
    for credentials in facebook_messenger_credentials:
        credentials_list = credentials.split(";")
        email = credentials_list[0]
        password = credentials_list[1]
        username = credentials_list[2]

    # Facebook Messenger login
    if registration_required:
        print("Logging in to Facebook Messenger...")
        os.system("adb shell svc wifi enable")
        time.sleep(7)
        os.putenv("email", email)
        os.putenv("password", password)
        os.system(
            "cd ~/Desktop/AndroidAnomalyDetection/FacebookMessengerShellScripts ; ./FacebookMessengerRegistration.sh")

    facebook_messenger_credentials.close()

    # Open Facebook Messenger's Self-Messaging
    subprocess.Popen(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerChats.xml ; newMessage=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="New message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerChats.xml) ; adb shell input tap $newMessage''',
        shell=True)
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
    subprocess.Popen(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelfMessage.xml ; msg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aa"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelfMessage.xml) ; adb shell input tap $msg''',
        shell=True)
    time.sleep(3)
    os.putenv("url", website)
    os.system("adb shell input text $url")
    time.sleep(3)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(3)
    website = website.rstrip("\n")
    formatted_messenger_url = website.replace("/", "\/")

    for x in range(3):
        log_file.write("Testing " + website.rstrip("\n") + " on Facebook Messenger (" + str(x + 1) + "/3)\n")
        os.system("adb logcat -c")
        adb_open_url_in_webview_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerOwnProfile.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="''' + formatted_messenger_url + '''"[^>]*content-desc=""[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerOwnProfile.xml) ; adb shell input tap $url'''
        subprocess.Popen(adb_open_url_in_webview_command, shell=True)
        time_countdown = 30.0
        while time_countdown > 0:
            start = time.time()
            result = android_webview_anomaly_checking(verification_text)
            end = time.time()
            if result == 3:
                elapsed_time = end - start
                time_countdown = time_countdown - elapsed_time
            else:
                break

        time.sleep(5)
        if result != 1:
            if result == 2:
                subprocess.Popen("adb shell input keyevent 4", shell=True)
                time.sleep(3)
            elif result == 3:
                log_file.write("Anomaly detected! Webpage was loaded but did not contain verification text!\n")

            adb_close_web_view_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerWebView.xml ; closeBrowser=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close browser"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerWebView.xml) ; adb shell input tap $closeBrowser'''
            subprocess.Popen(adb_close_web_view_command, shell=True)
        elif result == 1:
            time_counter = 30.0 - time_countdown
            log_file.write("Detected at "+str(time_counter)+" seconds\n")

        time.sleep(5)


# Reading file which contains the desired IM's package name and URL
url_file = open(home_path + "/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
log_file.write(
    "======================================== ANOMALY DETECTION ========================================\n\n")
for urls in url_file:
    url_list = urls.split(";")
    im = url_list[0]
    website = url_list[1]
    verification_text = url_list[2]

    if im == "com.facebook.orca":
        facebookmessenger(website, verification_text)

    time.sleep(5)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(3)
    subprocess.Popen(
        r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/RecentApps.xml ; closeRecentApps=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Close all"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/RecentApps.xml) ; adb shell input tap $closeRecentApps''',
        shell=True)
    log_file.write("\n===================================================================================================\n\n")
    time.sleep(5)

log_file.write("END")
url_file.close()
log_file.close()

print("Log file saved at ~/Desktop/AndroidAnomalyDetection/anomalydetectionlog"+str(serial_number)+".txt")
