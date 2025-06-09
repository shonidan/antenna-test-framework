from datetime import datetime
import pytest
import os
import json
import glob
import subprocess
from appium import webdriver
from get_caps import get_caps
import requests
import base64

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture(scope="function")
def caps():
    """Obtiene las desired capabilities desde get_caps.py y las guarda en tests/test_cache/caps.json"""
    caps_obj = get_caps()
    caps_dict = caps_obj.to_capabilities()

    # Crear carpeta tests/test_cache si no existe
    cache_dir = os.path.join("test_cache")
    os.makedirs(cache_dir, exist_ok=True)

    # Guardar el JSON
    cache_file = os.path.join(cache_dir, "caps.json")
    with open(cache_file, "w") as f:
        json.dump(caps_dict, f, indent=4)

    print(f"✅ Archivo caps.json guardado en: {os.path.abspath(cache_file)}")

    return caps_obj

@pytest.fixture(scope="function")
def driver(caps):
    apk_dir = os.path.join(os.path.dirname(__file__), "packages")
    apk_files = [f for f in os.listdir(apk_dir) if f.endswith(".apk")]

    if not apk_files:
        pytest.skip("❌ No APK found in packages folder")

    apk_path = os.path.join(apk_dir, apk_files[0])
    device_id = caps.device_name
    package = caps.app_package

    subprocess.run(["adb", "-s", device_id, "uninstall", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["adb", "-s", device_id, "install", apk_path], check=True)

    driver = webdriver.Remote("http://localhost:4723", options=caps)

    yield driver

    try:
        driver.quit()
    except Exception as e:
        print(f"⚠️ Warning: driver.quit() failed - {e}")

def screenshots_dir():
    """Crea la carpeta screenshots_dd_mm_aa dentro de tests si no existe y devuelve la ruta."""
    base_dir = os.path.dirname(__file__)
    fecha = datetime.now().strftime("%d_%m_%y")
    carpeta = f"screenshots_{fecha}"
    path = os.path.join(base_dir, "tests", carpeta)
    os.makedirs(path, exist_ok=True)
    return path

def clear_screenshots():
    """Borra todos los archivos .png dentro de screenshots."""
    path = screenshots_dir()
    files = glob.glob(os.path.join(path, "*.png"))
    for f in files:
        os.remove(f)

@pytest.fixture(autouse=True)
def clean_screenshots_before_test():
    """Fixture que limpia screenshots antes de cada test automáticamente."""
    clear_screenshots()
    yield
    # Si querés limpiar después del test también, podés poner clear_screenshots() acá.

@pytest.fixture
def screenshot(driver):
    def _take(name):
        path = screenshots_dir()
        filename = f"{name}.png"
        full_path = os.path.join(path, filename)
        driver.save_screenshot(full_path)
        print(f"Screenshot guardada: {full_path}")
    return _take

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_client_credentials_token(client_id, client_secret):
    auth = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

@pytest.fixture(scope="session")
def spotify_token():
    token = get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)
    return token