import os

lineUrl = "http://www.google.com"
print("Opening "+lineUrl+" using WebView in LINE...")
formattedLineUrl=lineUrl.replace("/", r"\/")
adbOpenUrlInWebViewCommand = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/KeepMemo.xml ; url=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="'''+formattedLineUrl+'''"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/KeepMemo.xml) ; adb shell input tap $url'''
os.system(adbOpenUrlInWebViewCommand)
print("Opened "+lineUrl+" using WebView in LINE")