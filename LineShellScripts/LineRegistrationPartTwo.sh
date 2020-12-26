adb shell input text $lineOtp
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
adb shell input text $linePassword
sleep 5
adb shell input keyevent 66 ; adb shell input keyevent 61 ; adb shell input keyevent 66
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
for i in `seq 1 5`; do adb shell input keyevent 61 ; done
sleep 5
adb shell input keyevent 160
sleep 5
adb shell input keyevent 160
