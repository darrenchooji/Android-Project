import subprocess

subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Webview.xml''',
                         shell=True)
verification_text = "Samsung"
verification_text = verification_text.replace("|", "\|")
adb_verify_custom_tab_activity_crash_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text=*"'''+verification_text+'''"*[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Webview.xml) ; echo $coords'''
verify = subprocess.Popen(adb_verify_custom_tab_activity_crash_command, shell=True, stdout=subprocess.PIPE)
verify_output = verify.stdout.read().decode("ascii")
print(verify_output)

