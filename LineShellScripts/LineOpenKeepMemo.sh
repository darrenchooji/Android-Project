adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Chats.xml ; keepmemo=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Keep Memo"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Chats.xml) ; adb shell input tap $keepmemo
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
