lineUrlInput = True
while lineUrlInput == True:
    lineUrl = input("Enter URL: ")
    isContinue = input("Do you want to continue (yes/no): ")
    if isContinue == "yes":
        lineUrlInput = True
    elif isContinue == "no":
        lineUrlInput = False
