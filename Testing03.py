import os
currentWorkingDirectory = os.getcwd()
sendSavedMessagesUrlFile = open(currentWorkingDirectory+"/URLs/urls.txt", "r")
for urls in sendSavedMessagesUrlFile:
    print(urls)