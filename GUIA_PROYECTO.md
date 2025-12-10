
# Guía del Proyecto: Detección de Fraude en Tarjetas de Crédito

Este proyecto implementa un sistema para detectar transacciones fraudulentas utilizando Machine Learning y lo expone mediante una API web.

## 📂 Estructura del Proyecto

*   **`Detección_de_Fraude...Dataset.ipynb`**: Tu notebook original con el análisis exploratorio de datos (EDA) y pruebas preliminares.
*   **`Entrenamiento_y_Modelo.ipynb`**: [NUEVO] Notebook limpio que realiza la configuración, entrenamiento definitivo del modelo y **guarda** los archivos necesarios (`model.pkl` y `scaler.pkl`) para que la API funcione.
*   **`backend/`**: Carpeta que contiene todo el código del sistema (API).
    *   `app.py`: El servidor API (Flask).
    *   `train_model.py`: Script alternativo para entrenar el modelo desde consola.
    *   `model.pkl` y `scaler.pkl`: Archivos binarios del modelo entrenado.
    *   `requirements.txt`: Lista de librerías necesarias.
    *   `Procfile`: Archivo para despliegue en la nube (Render/Heroku).

## 🚀 ¿Cómo probarlo localmente?

He creado un script automático para ti.

1.  Abre una terminal en la carpeta del proyecto.
2.  Ejecuta el siguiente comando:
    ```bash
    python prueba_local.py
    ```
3.  Este script hará lo siguiente automáticamente:
    *   Iniciará el servidor de la API en segundo plano.
    *   Enviará una transacción de prueba.
    *   Te mostrará el resultado (predicción de fraude).
    *   Cerrará el servidor.

Si ves un mensaje como `Status Code: 200` y una predicción, ¡todo funciona!

## ☁️ ¿Cómo subir a GitHub y Desplegar?

**Paso 1: GitHub**
Para que el proyecto esté listo, asegúrate de subir la carpeta `backend` completa. He creado un archivo `.gitignore` para evitar subir archivos innecesarios.

1.  Inicia un repositorio git: `git init`
2.  Agrega los archivos: `git add .`
3.  Haz commit: `git commit -m "Proyecto ML Detección Fraude"`
4.  Conecta tu repositorio remoto y haz `git push`.

**Paso 2: Despliegue (Ejemplo en Render.com)**
1.  Crea una cuenta en Render.com.
2.  Selecciona **"New Web Service"**.
3.  Conecta tu repositorio de GitHub.
4.  En la configuración:
    *   **Root Directory**: `backend` (Importante: indicar que la app está en esta carpeta).
    *   **Environment**: Python 3.
    *   **Start Command**: `gunicorn app:app` (Render lo leerá del Procfile, pero es bueno saberlo).
5.  Clic en "Create Web Service".

Render te dará una URL (ej. `https://mi-api.onrender.com`). Esa es la que entregarás en tu tarea.
Los parámetros para usarla son enviar un JSON POST a `/predict` con `Amount` y `V1`...`V28`.
