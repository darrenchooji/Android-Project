import subprocess
from pathlib import Path

home_path = str(Path.home())
url_file = open(home_path + "/Desktop/AndroidAnomalyDetection/URLs/urls.txt", "r")
for urls in url_file:
    url_list = urls.split(";")
    im = url_list[0]
    website = url_list[1]
    verification_text = url_list[2]
subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Webview.xml''',
                         shell=True)
verification_text = verification_text.replace("|", "\|")
verification_text = verification_text.replace("/", "\/")
print(verification_text)
adb_verify_custom_tab_activity_crash_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="'''+verification_text+'''"*[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Webview.xml) ; echo $coords'''
verify = subprocess.Popen(adb_verify_custom_tab_activity_crash_command, shell=True, stdout=subprocess.PIPE)
verify_output = verify.stdout.read().decode("ascii")
verify_output = verify_output.rstrip("\n")
print(verify_output)
if verify_output != '':
    print("OUTPUT")
else:
    print("NO OUTPUT")

