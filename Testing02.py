import subprocess

pull_telegram_chat_xml = subprocess.Popen(r'''adb pull $(adb shell uiautomator dump | grep -oP '[^ ]+.xml') /tmp/Chat.xml''', shell=True, stdout=subprocess.PIPE)
pull_telegram_chat_xml_output = pull_telegram_chat_xml.stdout.read().decode("ascii")
print(pull_telegram_chat_xml_output[:23])
