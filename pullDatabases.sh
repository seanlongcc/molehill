#copy database to easy location to pull from
#whatsapp
adb shell "su -c 'cp -rf /data/data/com.whatsapp/databases/wa.db sdcard/DCIM/'" 
adb shell "su -c 'cp -rf /data/data/com.whatsapp/databases/msgstore.db sdcard/DCIM/'"

#default contacts
adb shell "su -c 'cp -rf /data/data/com.android.providers.contacts/databases/contacts2.db sdcard/DCIM/'"

#fb messenger
adb shell "su -c 'cp -rf /data/data/com.facebook.orca/databases/threads_db2 sdcard/DCIM/'"
adb shell "su -c 'cp -rf /data/data/com.facebook.orca/databases/search_cache_db sdcard/DCIM/'"

#pull database from phone
#whatsapp
adb pull sdcard/DCIM/wa.db 
adb pull sdcard/DCIM/msgstore.db

#default contacts
adb pull sdcard/DCIM/contacts2.db

#fb messenger
adb pull sdcard/DCIM/threads_db2
adb pull sdcard/DCIM/search_cache_db

