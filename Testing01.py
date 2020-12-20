import subprocess, os

url = input("Enter a URL: ")
os.putenv("url", url)
os.system("adb shell input text $url")