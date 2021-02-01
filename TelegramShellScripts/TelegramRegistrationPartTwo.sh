adb -s $device_id shell input text $telegramOtp
sleep 5
adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 61 ; adb -s $device_id shell input keyevent 160
sleep 3
adb -s $device_id shell input keyevent 61
sleep 3
adb -s $device_id shell input keyevent 66
