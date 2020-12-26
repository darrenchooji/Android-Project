adb shell input text $telegramOtp
sleep 10
adb shell input keyevent 61 ; adb shell input keyevent 61 ; adb shell input keyevent 160
sleep 5
for i in `seq 1 3`; do adb shell input keyevent 61 ; done
sleep 5
adb shell input keyevent 160