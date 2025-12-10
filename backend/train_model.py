
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def train():
    print("Cargando dataset...")
    url = "https://raw.githubusercontent.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection/master/creditcard.csv"
    
    try:
        df = pd.read_csv(url)
    except Exception as e:
        print(f"Error al descargar: {e}")
        print("Generando datos sintéticos para demostración...")
        np.random.seed(42)
        n_samples = 10000
        data = {f'V{i}': np.random.normal(0, 1, n_samples) for i in range(1, 29)}
        data['Time'] = np.random.normal(0, 1, n_samples)
        data['Amount'] = np.random.exponential(100, n_samples)
        df = pd.DataFrame(data)
        # 1% fraud
        df['Class'] = 0
        fraud_idx = np.random.choice(n_samples, int(n_samples*0.01), replace=False)
        df.loc[fraud_idx, 'Class'] = 1

    # Preprocessing
    # Drop Time as it might not be relevant for generic prediction or needs complex handling
    # Scale Amount
    scaler = StandardScaler()
    df['Amount'] = scaler.fit_transform(df[['Amount']])
    
    # We will exclude Time for simplicity in the API, or keep it if required. 
    # Usually Time is relative to dataset start, so not useful for single API prediction unless transformed.
    # Let's drop Time.
    if 'Time' in df.columns:
        df = df.drop(['Time'], axis=1)

    X = df.drop('Class', axis=1)
    y = df['Class']

    print("Entrenando modelo...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    print("Guardando modelo y scaler...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("¡Listo!")

if __name__ == "__main__":
    train()
