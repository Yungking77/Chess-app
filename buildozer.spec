[app]
title = Chess App
package.name = chessapp
package.domain = org.yungking
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,python-chess
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 24
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
