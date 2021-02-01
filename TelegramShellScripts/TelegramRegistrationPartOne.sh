adb -s $device_id pull $(adb -s $device_id shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramIntroPage.xml ; coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Start Messaging"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramIntroPage.xml) ; adb -s $device_id shell input tap $coords
sleep 3
for i in `seq 1 3` ; do adb -s $device_id shell input keyevent 67 ; done
sleep 3
adb -s $device_id shell input text 65
sleep 3
adb -s $device_id shell input keyevent 61
sleep 3
adb -s $device_id shell input text $phoneNumber
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 66
