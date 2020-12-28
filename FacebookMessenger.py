import subprocess, time, sys, os, getpass

# Checking if Facebook Messenger is installed and installing the APK if required
checkFacebookMessengerInstallation = subprocess.Popen("adb shell pm list pacakges | grep com.facebook.orca", shell=True, stdout=subprocess.PIPE)
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
time.sleep(35)