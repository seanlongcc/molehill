#copy database to easy location to pull from
#viber
adb shell "su -c 'cp -rf /data/data/com.viber.voip/databases/viber_messages sdcard/DCIM/'"
adb shell "su -c 'cp -rf /data/data/com.viber.voip/databases/viber_data sdcard/DCIM/'"

#signal
adb shell "su -c 'cp -rf /storage/emulated/0/Signal/Backups sdcard/DCIM/'"

#telegram
adb shell "su -c 'cp -rf /data/data/org.telegram.messenger/files/cache4.db sdcard/DCIM/'" 

#pull database from phone
#viber
adb pull sdcard/DCIM/viber_messages
adb pull sdcard/DCIM/viber_data

#signal
adb pull sdcard/DCIM/Backups

#telegram
adb pull sdcard/DCIM/cache4.db 