import subprocess
import time


subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/TelegramWebview.xml ; 
coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /resource-id="com.android.chrome:id\/menu_button"[
^>]*content-desc="More options"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/TelegramWebview.xml) ; adb shell 
input tap $coords''', shell=True)
time.sleep(3)


subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/MoreOptionsTab.xml ; 
coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /resource-id="com.android.chrome:id\/menu_item_text"[
^>]*content-desc="Open in Chrome"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/MoreOptionsTab.xml) ; adb 
shell input tap $coords''', shell=True)
time.sleep(3)


subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Chrome.xml ; coords=$(perl 
-ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /resource-id="com.android.chrome:id\/url_bar"[^>]*bounds="\[(\d+),
(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Chrome.xml) ; adb shell input tap $coords''', shell=True)
time.sleep(3)

subprocess.Popen("adb shell input text Inspect%sElement", shell=True)
# Open Inspect Element Bookmark --> Need to do

adb_open_inspect_element_on_chrome_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') 
/tmp/Chrome.xml ; coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text=""[^>]*bounds="\[(\d+),
(\d+)\]\[(\d+),(\d+)\]"/' /tmp/Chrome.xml) ; adb shell input tap $coords '''
subprocess.Popen(adb_open_inspect_element_on_chrome_command, shell=True)
time.sleep(3)


adb_open_inspect_element_network_tab_command = r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') 
/tmp/InspectElement.xml ; coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Network"[^>]*bounds="\[
(\d+),(\d+)\]\[(\d+),(\d+)\]"/' /tmp/InspectElement.xml) ; adb shell input tap $coords '''
subprocess.Popen(adb_open_inspect_element_network_tab_command, shell=True)
