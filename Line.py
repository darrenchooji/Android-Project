import subprocess

checkLineInstallation = subprocess.Popen("adb shell pm list packages | grep jp.naver.line.android", shell=True, stdout=subprocess.PIPE)
checkLineInstallationOutput = checkLineInstallation.stdout.read().decode("ascii")
if checkLineInstallationOutput == '':
    print("LINE is not installed. Installing LINE Now...")
    subprocess.run("adb install ~/Desktop/APKs/line-10-21-3.apk", shell=True)
    print("LINE installlation finished")
else:
    print("LINE is installed")

