[app]

# This .spec config file tells Buildozer an app's requirements for being built.

#

# Sindhi Dictionary Android Application

#

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

#

# Python itself is supplied by python-for-android.

#

requirements = python3,kivy

# (str) Custom source folders for requirements

# requirements.source.kivy = ../../kivy

# (str) Presplash

#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon

#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations

orientation = portrait

# (bool) Fullscreen

fullscreen = 0

#

# OSX Specific

#

# Kivy version to use on macOS

osx.kivy_version = 2.3.1

#

# Android specific

#

# (bool) Indicate if application is fullscreen

# fullscreen = 0

# ---------------------------------------------------------

# Android SDK

# ---------------------------------------------------------

# Target Android API

android.api = 35

# Minimum Android API

android.minapi = 24

# Android SDK version

android.sdk = 35

# Android NDK version

android.ndk = 28c

# Android NDK API

android.ndk_api = 24

# Automatically accept Android SDK license agreements

android.accept_sdk_license = True

# SDK path is automatically managed by Buildozer

#android.sdk_path =

# NDK path is automatically managed by Buildozer

#android.ndk_path =

# ANT path is automatically managed by Buildozer

#android.ant_path =

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

# Android architecture

# ---------------------------------------------------------

# Modern 64-bit ARM plus 32-bit ARM support

android.archs = arm64-v8a,armeabi-v7a

# ---------------------------------------------------------

# Android artifact

# ---------------------------------------------------------

# Debug build produces APK

android.debug_artifact = apk

# Release build produces APK

android.release_artifact = apk

# ---------------------------------------------------------

# Android backup

# ---------------------------------------------------------

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

#

# iOS specific

#

# Path to custom kivy-ios folder

#ios.kivy_ios_dir = ../kivy-ios

# Kivy iOS repository

ios.kivy_ios_url = https://github.com/kivy/kivy-ios

# Kivy iOS branch

ios.kivy_ios_branch = master

# ios-deploy repository

ios.ios_deploy_url = https://github.com/phonegap/ios-deploy

# ios-deploy branch

ios.ios_deploy_branch = 1.12.2

# Disable iOS code signing

ios.codesign.allowed = false

#

# iOS additional options

#

#ios.codesign.debug =
#ios.codesign.development_team.debug =
#ios.codesign.release =
#ios.codesign.development_team.release =

#ios.media_usage_description =
#ios.local_network_usage_description =
#ios.camera_usage_description =

#ios.viewcontroller_based_statusbar_appearance = False

#

# Buildozer

#

[buildozer]

# Log level

#

# 0 = errors only

# 1 = normal

# 2 = detailed

#

log_level = 2

# Do not display root warning

warn_on_root = 0

# Build artifact storage

build_dir = ./.buildozer

# APK/AAB output directory

bin_dir = ./bin

#

# ---------------------------------------------------------

# Additional Android configuration options

# ---------------------------------------------------------

#

# Presplash background color

#android.presplash_color = #FFFFFF

# Adaptive icon

#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# Android features

#android.features = android.hardware.usb.host

# Android extra manifest

#android.extra_manifest_xml =

# Android extra application arguments

#android.extra_manifest_application_arguments =

# Android service class

#android.service_class_name = org.kivy.android.PythonService

# Android activity class

#android.activity_class_name = org.kivy.android.PythonActivity

# Android whitelist

#android.whitelist =

# Android blacklist

#android.blacklist =

# Android whitelist source

#android.whitelist_src =

# Android blacklist source

#android.blacklist_src =

#

# ---------------------------------------------------------

# Java / Android libraries

# ---------------------------------------------------------

#

# Java JAR files

#android.add_jars =

# Java source files

#android.add_src =

# Android AAR files

#android.add_aars =

# Android assets

#android.add_assets =

# Android resources

#android.add_resources =

# Gradle dependencies

#android.gradle_dependencies =

# AndroidX

#android.enable_androidx = True

# Java compile options

#android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# Gradle repositories

#android.add_gradle_repositories =

# Packaging options

#android.add_packaging_options =

# Java activities

#android.add_activities =

#

# ---------------------------------------------------------

# Android manifest

# ---------------------------------------------------------

#

# OUYA category

#android.ouya.category = GAME

# OUYA icon

#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# Manifest intent filters

#android.manifest.intent_filters =

# XML resources

#android.res_xml =

# Launch mode

#android.manifest.launch_mode = standard

# Screen orientation

#android.manifest.orientation = portrait

#

# ---------------------------------------------------------

# Android native libraries

# ---------------------------------------------------------

#

# ARM libraries

#android.add_libs_armeabi = libs/android/*.so

# ARM v7 libraries

#android.add_libs_armeabi_v7a = libs/android-v7/*.so

# ARM 64 libraries

#android.add_libs_arm64_v8a = libs/android-v8/*.so

# x86 libraries

#android.add_libs_x86 = libs/android-x86/*.so

# x86_64 libraries

#android.add_libs_x86_64 = libs/android-x86_64/*.so

#

# ---------------------------------------------------------

# Android runtime

# ---------------------------------------------------------

#

# Copy libraries instead of libpymodules.so

android.copy_libs = 1

# Keep screen awake

android.wakelock = False

# Android logcat filters

#android.logcat_filters = *:S python:D

# Android logcat PID only

#android.logcat_pid_only = False

# Additional ADB arguments

#android.adb_args =

# Application metadata

#android.meta_data =

# Android library references

#android.library_references =

# Android uses-library

#android.uses_library =

#

# ---------------------------------------------------------

# Android additional settings

# ---------------------------------------------------------

#

# Numeric version code

#android.numeric_version = 1

# Disable Python byte compilation

#android.no-byte-compile-python = False

# Display cutout

#android.display_cutout = never

# Manifest placeholders

#android.manifest_placeholders = [:]

#

# ---------------------------------------------------------

# Python-for-Android settings

# ---------------------------------------------------------

#

# Custom p4a URL

#p4a.url =

# p4a fork

p4a.fork = kivy

# p4a branch

p4a.branch = master

# p4a commit

#p4a.commit = HEAD

# p4a source directory

#p4a.source_dir =

# p4a local recipes

#p4a.local_recipes =

# p4a hook

#p4a.hook =

# p4a bootstrap

p4a.bootstrap = sdl2

# p4a port

#p4a.port =

# Use setup.py

#p4a.setup_py = false

# Extra p4a arguments

#p4a.extra_args =

#

# ---------------------------------------------------------

# General notes

# ---------------------------------------------------------

#

# Buildozer uses ConfigParser-style syntax.

#

# Configuration values must not be indented.

#

# Comments cannot be placed after configuration values.

#

# Correct:

#

# title = Sindhi Dictionary

#

# Incorrect:

#

# title = Sindhi Dictionary # comment

#

# Lists are comma-separated.

#

# Example:

#

# source.include_exts = py,png,jpg,csv,json

#

# Environment variables can override Buildozer options.

#

# Example:

#

# BUILDOZER_WARN_ON_ROOT=0

#

# Build profiles are also supported.

#

# Example:

#

# buildozer --profile demo android debug

#

# ---------------------------------------------------------
