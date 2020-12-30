import subprocess, time, sys, os, getpass

# Checking if Facebook Messenger is installed and installing the APK if required
checkFacebookMessengerInstallation = subprocess.Popen("adb shell pm list packages | grep com.facebook.orca", shell=True, stdout=subprocess.PIPE)
checkFacebookMessengerInstallationOutput = checkFacebookMessengerInstallation.stdout.read().decode("ascii")
if checkFacebookMessengerInstallationOutput == '':
    print("Facebook Messenger is not installed. Installing Facebook Messenger now...")
    subprocess.run("adb install ~/Desktop/APKs/messenger*.apk", shell=True)
    print("Facebook Messenger installation finished")
else:
    print("Facebook Messenger is already installed")

# Check if login is required
registrationRequired = True
subprocess.run("adb logcat -c", shell=True)
subprocess.run("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity", shell=True)
time.sleep(30)
checkFacebookMessengerRegistrationRequired = subprocess.Popen("adb logcat -d ActivityTaskManager:I *:S | grep com.facebook.orca/com.facebook.messaging.accountlogin.AccountLoginActivity", shell=True, stdout=subprocess.PIPE)
checkFacebookMessengerRegistrationRequiredOutput = checkFacebookMessengerRegistrationRequired.stdout.read().decode("ascii")
if checkFacebookMessengerRegistrationRequiredOutput != '':
    registrationRequired = True
    print("Facebook Messenger login required")
else:
    registrationRequired = False
    print("Facebook Messenger login not required")

currentWorkingDirectory = os.getcwd()
facebookMessengerCredentials = open(currentWorkingDirectory+"/Credentials/FacebookMessenger.txt", "r")
for credentials in facebookMessengerCredentials:
    credentialsList = credentials.split(";")
    email = credentialsList[0]
    password = credentialsList[1]
    username = credentialsList[2]

# Facebook Messenger login
if registrationRequired == True:
    print("Logging in to Facebook Messenger...")
    os.putenv("email", email)
    os.putenv("password", password)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/FacebookMessengerShellScripts ; ./FacebookMessengerRegistration.sh")

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
os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerChats.xml ; newMessage=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="New Message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerChats.xml) ; adb shell input tap $newMessage''')
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

# Reading a text file of URLs and sending those URLs to own profile and open those URLs using WebView on Facebook Messenger
urlFile = open(currentWorkingDirectory+"/URLs/urls.txt", "r")
for messengerUrl in urlFile:
    os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelfMessage.xml ; msg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aa"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelfMessage.xml) ; adb shell input tap $msg''')
    time.sleep(5)
    os.putenv("url", messengerUrl)
    os.system("adb shell input text $url")
    time.sleep(10)
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66")
    time.sleep(5)
    os.system("adb shell input keyevent 4")
    time.sleep(5)
    messengerUrl = messengerUrl.rstrip("\n")
    formattedMessengerUrl = messengerUrl.replace("/", "\/")
    print("Opening " + messengerUrl + " using WebView on Facebook Messenger...")
    adbOpenUrlInWebviewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerOwnProfile.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="'''+formattedMessengerUrl+'''"[^>]*content-desc=""[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerOwnProfile.xml) ; adb shell input tap $url'''
    os.system(adbOpenUrlInWebviewCommand)
    print("Opened " + messengerUrl + " using WebView on Facebook Messenger")
    time.sleep(45)
    adbCloseWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MessengerWebView.xml ; closeBrowser=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Close browser"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MessengerWebView.xml) ; adb shell input tap $closeBrowser'''
    os.system(adbCloseWebViewCommand)
    print("Closing "+messengerUrl)
    time.sleep(20)

urlFile.close()