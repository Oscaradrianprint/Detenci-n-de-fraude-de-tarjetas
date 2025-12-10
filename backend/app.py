
from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Cargar modelo y scaler
print("Cargando modelo...")
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("Modelo cargado exitosamente.")
except FileNotFoundError:
    print("Error: No se encontró model.pkl o scaler.pkl. Asegúrese de haber ejecutado train_model.py primero.")
    model = None
    scaler = None

@app.route('/')
def home():
    return "API de Detección de Fraude en Tarjetas de Crédito. Use /predict para realizar predicciones."

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not scaler:
        return jsonify({'error': 'Modelo no disponible'}), 500
    
    try:
        data = request.get_json()
        
        # Validar entrada
        # Esperamos 'Amount' y 'V1'...'V28'
        # Si envían una lista de características, la extraemos
        
        # Ejemplo de entrada simple: {"Amount": 100.0, "V1": 0.5, ... "V28": -0.1}
        # O lista de valores
        
        # Vamos a asumir que envían un diccionario con las features necesarias
        # Primero convertir a DataFrame para facilitar el uso del scaler y garantizar orden si usamos nombres
        
        # Crear input array
        # El modelo fue entrenado con: V1...V28, Amount (scaled) (orden depende de como quedo el DF en train)
        # En train_model.py: 
        # data = {f'V{i}': ... for i in range(1, 29)} -> V1...V28
        # data['Amount'] = ...
        # df = pd.DataFrame(data) -> Orden de columnas: V1, V2... V28, Amount (o similar)
        # El orden en dictionary data = {...} es inserción en Python 3.7+, pero 'V1' a 'V28' y 'Amount'.
        
        # Lo mejor es asegurar el orden.
        # Las columnas esperadas son V1...V28 y Amount.
        
        expected_cols = [f'V{i}' for i in range(1, 29)] + ['Amount']
        
        input_data = {}
        for col in expected_cols:
            if col not in data:
                return jsonify({'error': f'Falta el campo {col}'}), 400
            input_data[col] = float(data[col])
            
        # Crear DF para un solo registro
        df_input = pd.DataFrame([input_data])
        
        # Escalar Amount
        df_input['Amount'] = scaler.transform(df_input[['Amount']])
        
        # Reordenar columnas para coincidir con entrenamiento (aseguramos el orden específico)
        # Si el modelo es sklearn, usa numpy array y espera el mismo orden que fit.
        # En train_model.py: df.drop('Class') -> el orden es V1...V28, Time, Amount. Y Time lo quitamos.
        # Entonces V1...V28, Amount. (Porque Amount se agregó al final en el dict comprehension + assignments)
        
        # Forzamos el orden
        df_input = df_input[expected_cols]
        
        prediction = model.predict(df_input)
        probability = model.predict_proba(df_input)[0][1]
        
        result = {
            'prediction': int(prediction[0]), # 0 o 1
            'is_fraud': bool(prediction[0] == 1),
            'fraud_probability': float(probability)
        }
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
