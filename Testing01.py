import subprocess

adb_verify_custom_tab_activity_crash_command = r'''coords=$(perl -ne 'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="Aw, Snap!"[^>]*resource-id="com.android.chrome:id\/sad_tab_title"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/' ~/Desktop/TelegramAwSnap.xml) ; echo $coords'''
subprocess.Popen(adb_verify_custom_tab_activity_crash_command, shell=True)
