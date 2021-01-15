adb shell input text $email
sleep 3
adb shell input keyevent 61
sleep 3
adb shell input text $password
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 10
adb shell input keyevent 66
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 3
adb shell input keyevent 66
sleep 7
adb shell svc wifi disable
sleep 3
adb shell input keyevent KEYCODE_APP_SWITCH
sleep 5
adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/RecentApps.xml ; closeRecentApps=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Close all"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/RecentApps.xml) ; adb shell input tap $closeRecentApps
sleep 5
adb shell am start -n com.facebook.orca/.auth.StartScreenActivity
sleep 15