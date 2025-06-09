
# PinApp Automation framework

Requisitos previos

Tener instalados los siguientes paquetes:

    JDK 8 (jdk8-openjdk)

    Android SDK (android-sdk, android-sdk-platform-tools, android-sdk-platforms)

    Node.js y npm (nodejs, npm)

Instalacion de dependencias Python:

    pip install -r requirements.txt

Instalacion de Appium drivers para Android:

    npm install -g appium
    appium driver install uiautomator2

Configuración

Creacion de archivo .env en la raíz del proyecto con credenciales extraidas de Spotify https://developer.spotify.com/:

    SPOTIFY_CLIENT_ID=tu-client-id
    SPOTIFY_CLIENT_SECRET=tu-client-secret

Como correr los test:
Dispositivo android debe tener dubbug prendido y certificados autorizados.
Conectar dispositivo android y ejecutar en consola:

    appium


En otra terminal correr:
    
    pytest tests/

El conftest detecta por medio de ADB los desired caps para las pruebas en entorno local.