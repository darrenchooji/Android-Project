import os
currentWorkingDirectory = os.getcwd()
credentials = open(currentWorkingDirectory+"/Credentials/FacebookMessenger.txt", "r")
for credentialsInfo in credentials:
    credentialsInfoList = credentialsInfo.split(";")
    email = credentialsInfoList[0]
    password = credentialsInfoList[1]
    username = credentialsInfoList[2]

print(email)
print(password)
print(username)



