# copy database to easy location to pull from
#whatsapp
adb shell "su -c 'cp -rf /data/data/com.whatsapp/databases/wa.db sdcard/DCIM/'" 
adb shell "su -c 'cp -rf /data/data/com.whatsapp/databases/msgstore.db sdcard/DCIM/'"

#default contacts
adb shell "su -c 'cp -rf /data/data/com.android.providers.contacts/databases/contacts2.db sdcard/DCIM/'"

#fb messenger
adb shell "su -c 'cp -rf /data/data/com.facebook.orca/databases/threads_db2 sdcard/DCIM/'"
adb shell "su -c 'cp -rf /data/data/com.facebook.orca/databases/search_cache_db sdcard/DCIM/'"

#viber
adb shell "su -c 'cp -rf /data/data/com.viber.voip/databases/viber_messages sdcard/DCIM/'"
adb shell "su -c 'cp -rf /data/data/com.viber.voip/databases/viber_data sdcard/DCIM/'"

#signal
adb shell "su -c 'cp -rf /storage/emulated/0/Signal/Backups sdcard/DCIM/'"

#telegram
adb shell "su -c 'cp -rf /data/data/org.telegram.messenger/files/cache4.db sdcard/DCIM/'" 

# pull database from phone
#whatsapp
adb pull sdcard/DCIM/wa.db 
adb pull sdcard/DCIM/msgstore.db

#default contacts
adb pull sdcard/DCIM/contacts2.db

#fb messenger
adb pull sdcard/DCIM/threads_db2
adb pull sdcard/DCIM/search_cache_db

#viber
adb pull sdcard/DCIM/viber_messages
adb pull sdcard/DCIM/viber_data

#signal
adb pull sdcard/DCIM/Backups

#telegram
adb pull sdcard/DCIM/cache4.db 