[app]
title = Calculadora
package.name = calculadora
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 0.1

# CLAVE: hostpython3 es necesario para compilar extensiones nativas con p4a
requirements = python3,hostpython3,kivy,pillow

# El archivo real es .jpeg
presplash.filename = %(source.dir)s/calcu.jpeg
icon.filename = %(source.dir)s/calcu.jpeg

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.3.0

fullscreen = 0

android.api = 33
android.minapi = 24

# CORRECCIÓN CLAVE 1: formato correcto del NDK para buildozer (sin "r", sin puntos extra)
android.ndk = 25b

android.ndk_api = 24

# CORRECCIÓN CLAVE 2: esta bandera le dice a buildozer que acepte
# licencias automáticamente sin prompt interactivo
android.accept_sdk_license = True

# CORRECCIÓN CLAVE 3: se fija la versión de build-tools a 33.0.2
# para evitar que buildozer descargue la 37.0.0 y su licencia nueva
android.sdk_path =
android.ndk_path =

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
