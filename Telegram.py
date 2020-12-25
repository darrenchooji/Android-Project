import subprocess, time, sys, os, getpass
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
    print("Logging in to LINE...")
    phoneNumber = input("Enter phone number: ")
    os.putenv("phoneNumber", phoneNumber)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartOne.sh")
    telegramOtp = input("Enter Telegram OTP: ")
    os.putenv("telegramOtp", telegramOtp)
    os.system("cd ~/Desktop/AndroidAnomalyDetection/TelegramShellScripts ; ./TelegramRegistrationPartTwo.sh")
