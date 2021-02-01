adb -s $device_id shell input text $email
sleep 3
adb -s $device_id shell input keyevent 61
sleep 3
adb -s $device_id shell input text $password
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 66
sleep 10
adb -s $device_id shell input keyevent 66
sleep 5
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 66
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 66
sleep 3
adb -s $device_id shell input keyevent 66
sleep 7
adb -s $device_id shell svc wifi disable
sleep 3
adb -s $device_id shell input keyevent KEYCODE_APP_SWITCH
sleep 5
adb -s $device_id pull $(adb -s $device_id shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/RecentApps.xml ; closeRecentApps=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Close all"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/RecentApps.xml) ; adb -s $device_id shell input tap $closeRecentApps
sleep 5
adb -s $device_id shell am start -n com.facebook.orca/.auth.StartScreenActivity
sleep 15
