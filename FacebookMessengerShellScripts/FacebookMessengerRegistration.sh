adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/FbMessengerLogin.xml ; inputEmail=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /content-desc="Phone Number or Email"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/FbMessengerLogin.xml) ; adb shell input tap $inputEmail
sleep 3
adb shell input text $email
sleep 5
adb shell input keyevent 61
sleep 5
adb shell input text $password
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 60
adb shell input keyevent 66
sleep 20
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 20
