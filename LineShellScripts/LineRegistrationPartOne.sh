adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 160
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 160
sleep 3
adb -s $device_id shell input keyevent 160
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 160
sleep 3
adb -s $device_id pull $(adb -s $device_id shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/SelectCountry.xml ; sg=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Singapore"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/SelectCountry.xml) ; adb -s $device_id shell input tap $sg
sleep 3
adb -s $device_id shell input text $phone_number
sleep 3
adb -s $device_id shell input keyevent 160 ; adb -s $device_id shell input keyevent 66
sleep 3
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 160
