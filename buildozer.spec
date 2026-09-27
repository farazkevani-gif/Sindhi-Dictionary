[app]

# (str) Title of your application
title = Sindhi Dictionary

# (str) Package name
package.name = sindhidictionary

# (str) Package domain
package.domain = org.farazkevani

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,csv,json,txt,ttf,db

# (list) Explicit files/directories to include
source.include_patterns = dictionary_stage14_grouped.csv,dictionary_stage18_reverse_index.json,dictionary_stage22_android.db,fonts/*.ttf,Noto_Sans_Arabic/*.ttf

# (list) List of directories to exclude
source.exclude_dirs = .git,.github,.buildozer,bin,**pycache**,tests,venv,.venv

# (list) Exclude unnecessary development files
source.exclude_patterns = *.pyc,*.pyo,*.bak,*.save,*_backup.py,*_review.csv,*_audit.csv,*_candidates.csv,*_rejected.csv,*_removed.csv,*_review.txt

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3,kivy,charset-normalizer==3.3.2

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# OSX Specific
osx.kivy_version = 2.3.1

# ---------------------------------------------------------
# Android SDK / NDK
# ---------------------------------------------------------

# Target Android API
android.api = 34

# Minimum Android API
android.minapi = 24

# Android SDK version
android.sdk = 34

# Android NDK version
android.ndk = 25b

# Android NDK API
android.ndk_api = 24

# Automatically accept Android SDK license agreements
android.accept_sdk_license = True

# Do not skip SDK updates
android.skip_update = False

# ---------------------------------------------------------
# Android application
# ---------------------------------------------------------

# Default Kivy Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# Android application theme
android.apptheme = "@android:style/Theme.NoTitleBar"

# Screen orientation
android.manifest.orientation = portrait

# Keep screen from sleeping
android.wakelock = False

# Android permissions
android.permissions = android.permission.INTERNET

# ---------------------------------------------------------
# Android architecture & artifacts
# ---------------------------------------------------------

# Modern 64-bit ARM plus 32-bit ARM support
android.archs = arm64-v8a,armeabi-v7a

# Debug build produces APK
android.debug_artifact = apk

# Release build produces APK
android.release_artifact = apk

# Android backup
android.allow_backup = True

# ---------------------------------------------------------
# Python for Android
# ---------------------------------------------------------

# Official Kivy python-for-android
p4a.fork = kivy

# Use master branch
p4a.branch = master

# SDL2 bootstrap for Kivy
p4a.bootstrap = sdl2

# Copy libraries instead of libpymodules.so
android.copy_libs = 1

# ---------------------------------------------------------
# Buildozer settings
# ---------------------------------------------------------

[buildozer]

# Log level (2 = detailed)
log_level = 2

# Do not display root warning
warn_on_root = 0

# Build artifact storage
build_dir = ./.buildozer

# APK/AAB output directory
bin_dir = ./bin
