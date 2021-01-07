import subprocess, time

adb_check_webpage_availibility_command = r'''webpageavailability=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Webpage not available"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/OpenedWebviewPage.xml) ; echo $webpageavailability'''
subprocess.run(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/OpenedWebviewPage.xml''', shell=True)
get_webpage_availability = subprocess.Popen(adb_check_webpage_availibility_command, shell=True, stdout=subprocess.PIPE)
time.sleep(3)
get_webpage_availability_output = get_webpage_availability.stdout.read().decode("ascii")
get_webpage_availability_output = get_webpage_availability_output.rstrip("\n")
if get_webpage_availability_output == '':
    print("Webpage can be shown")
else:
    print("Webpage cannot be shown")
