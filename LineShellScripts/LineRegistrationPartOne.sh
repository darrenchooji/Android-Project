adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input keyevent 160
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelectCountry.xml ; sg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Singapore"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelectCountry.xml) ; adb shell input tap $sg
sleep 3
adb shell input text $phoneNumber
sleep 3
adb shell input keyevent 160 ; adb shell input keyevent 66
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
