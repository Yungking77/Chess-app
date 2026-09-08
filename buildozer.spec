[app]
title = Chess App
package.name = chessapp
package.domain = org.yungking
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,python-chess
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
