adb shell input text $lineOtp
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 3
adb shell input text $linePassword
sleep 3
adb shell input keyevent 66 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 3
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
sleep 3
adb shell input keyevent 61 ; adb shell input keyevent 160
