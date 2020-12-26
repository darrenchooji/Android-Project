adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramIntroPage.xml ; coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Start Messaging"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramIntroPage.xml) ; adb shell input tap $coords
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
for i in `seq 1 4`; do adb shell input keyevent 61 ; done
sleep 5
adb shell input keyevent 160
sleep 5
for i in `seq 1 3` ; do adb shell input keyevent 67 ; done
sleep 5
adb shell input text 65
sleep 5
adb shell input keyevent 61
sleep 5
adb shell input text $phoneNumber
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
for i in `seq 1 3`; do adb shell input keyevent 61 ; done
sleep 5
adb shell input keyevent 66
sleep 5
adb shell input keyevent 66
