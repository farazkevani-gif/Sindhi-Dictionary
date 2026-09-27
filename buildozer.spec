```ini
[app]

# =========================================================
# APPLICATION
# =========================================================

title = Sindhi Dictionary

package.name = sindhidictionary

package.domain = org.farazkevani

source.dir = .

version = 1.0


# =========================================================
# FILES INCLUDED IN APK
# =========================================================

source.include_exts = py,png,jpg,jpeg,kv,atlas,csv,json,ttf,txt

source.exclude_dirs = .git,.buildozer,bin,__pycache__,venv


# =========================================================
# PYTHON / KIVY
# =========================================================

requirements = python3==3.11.5,kivy


# =========================================================
# SCREEN
# =========================================================

orientation = portrait

fullscreen = 0


# =========================================================
# ANDROID SDK
# =========================================================

android.api = 35

android.minapi = 24

android.sdk = 35

android.sdk_path = /opt/android-sdk


# =========================================================
# ANDROID NDK
# =========================================================

android.ndk = 28c

android.ndk_api = 24


# =========================================================
# ANDROID BUILD
# =========================================================

android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

android.copy_libs = 1

android.allow_backup = True


# =========================================================
# ANDROID ACTIVITY
# =========================================================

android.entrypoint = org.kivy.android.PythonActivity


# =========================================================
# BUILDOZER
# =========================================================

[buildozer]

log_level = 2

warn_on_root = 0
```
