import subprocess, time, sys, os, getpass

# Checking if LINE is installed and installing the LINE APK if required
checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
if checkLineInstallationOutput == '':
    print("LINE is not installed. Installing LINE Now...")
    subprocess.run("adb install ~/Desktop/APKs/line-10-21-3.apk", shell=True)
    print("LINE installation finished")
else:
    print("LINE is installed")

# Check if login to LINE is required
registrationRequired = True
subprocess.run("adb logcat -c", shell=True)
subprocess.run("adb shell am start -n jp.naver.line.android/.activity.SplashActivity", shell=True)
time.sleep(25)
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

# Running LINE login script (Only if registrationRequired=True)
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
print("LINE's Keep Memo Opened")
if registrationRequired == True:
    os.system("adb shell input keyevent 61 ; adb shell input keyevent 160")

# Prompt for URL input and send that input to Keep Memo (Self-Messaging)
lineUrl = input("Enter URL: ")
os.putenv("lineUrl", lineUrl)
os.system("adb shell input text $url ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160")
time.sleep(5)

#

