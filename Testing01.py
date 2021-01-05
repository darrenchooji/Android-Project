from pathlib import Path
import os
home = str(Path.home())
telegramCredentials = open(home + "/Desktop/Credentials/FacebookMessenger.txt", "r")
for credentials in telegramCredentials:
    credentialsList = credentials.split(";")
    phoneNumber = credentialsList[0]
os.putenv("phoneNumber", phoneNumber)
os.system("echo $phoneNumber")