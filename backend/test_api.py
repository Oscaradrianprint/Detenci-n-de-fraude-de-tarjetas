
import requests
import numpy as np

url = 'http://127.0.0.1:5000/predict'

# Generar datos aleatorios
data = {f'V{i}': np.random.normal() for i in range(1, 29)}
data['Amount'] = 100.0

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
