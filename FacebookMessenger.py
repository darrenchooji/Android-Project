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
os.system("nmcli networking off")
os.system("adb shell input keyevent KEYCODE_APP_SWITCH")
time.sleep(15)
os.system("adb shell input keyevent DEL")
time.sleep(15)
os.system("adb shell am start -n com.facebook.orca/.auth.StartScreenActivity")
time.sleep(30)
os.system(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerChats.xml ; newMessage=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="New Message"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerChats.xml) ; adb shell input tap $newMessage''')
time.sleep(10)
os.system("nmcli networking on")






