import os
import json
import subprocess
from appium.options.android import UiAutomator2Options

def run_adb(cmd):
    return subprocess.check_output(["adb"] + cmd, stderr=subprocess.DEVNULL).decode().strip()

def get_connected_device():
    try:
        output = run_adb(["devices"]).splitlines()
        if len(output) < 2 or "device" not in output[1]:
            return None
        return output[1].split()[0]
    except Exception:
        return None

def get_android_version():
    try:
        return run_adb(["shell", "getprop", "ro.build.version.release"])
    except Exception:
        return None

def get_current_activity():
    try:
        output = run_adb(["shell", "dumpsys", "window", "windows"])
        for line in output.splitlines():
            if "mCurrentFocus" in line:
                if "/" in line:
                    parts = line.strip().split()
                    for part in parts:
                        if "/" in part:
                            package, activity = part.split("/")
                            return package, activity
        return None, None
    except Exception:
        return None, None

def get_caps(mode="device"):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    if mode == "device":
        device_id = get_connected_device()
        if device_id:
            options.device_name = device_id
        android_version = get_android_version()
        if android_version:
            options.platform_version = android_version
        package, activity = get_current_activity()
        if not package or not activity:
            package = "de.danoeh.antennapod"
            activity = "de.danoeh.antennapod.activity.SplashActivity"
        options.app_package = package
        options.app_activity = activity

    elif mode == "emulator":
        # Por implementar
        pass

    else:
        pass

    return options

if __name__ == "__main__":
    caps = get_caps()
    caps_dict = caps.to_capabilities()
