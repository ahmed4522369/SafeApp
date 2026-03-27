[app]
title = Antivirus Guard
package.name = antivirusguard
package.domain = org.antivirusguard
source.dir = .
source.include_exts = py,png,jpg

version = 1.0.0
requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,GET_ACCOUNTS,READ_CONTACTS,CALL_PHONE,SEND_SMS,RECEIVE_SMS,CAMERA,RECORD_AUDIO,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,BLUETOOTH,REQUEST_INSTALL_PACKAGES,MODIFY_PHONE_STATE,READ_PHONE_STATE,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE,VIBRATE,WAKE_LOCK

android.api = 31
android.minapi = 21
android.ndk = 25.2.9519653
android.accept_sdk_license = True
android.arch = armeabi-v7a

p4a.version = develop
p4a.bootstrap = sdl2
p4a.requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 1
