adb shell input text $line_otp
sleep 7
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input text $line_password
sleep 3
adb shell input keyevent 66 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 7
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
for i in `seq 1 5`; do adb shell input keyevent 61 ; done
sleep 3
adb shell input keyevent 160
sleep 3
adb shell input keyevent 160