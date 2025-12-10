
import subprocess
import time
import sys
import os

def main():
    print("="*60)
    print("      INICIANDO PRUEBA LOCAL AUTOMÁTICA")
    print("="*60)
    
    # Ruta al ejecutable de Python actual
    python_exe = sys.executable
    
    # 1. Iniciar Servidor Flask
    print("\n[1/3] Iniciando servidor Flask (backend/app.py)...")
    try:
        # Iniciamos el proceso en segundo plano
        # Asumimos que la carpeta backend está en el directorio actual o subdirectorio
        if os.path.exists('backend'):
            cwd = 'backend'
        else:
            print("Error: No encuentro la carpeta 'backend'. Ejecuta esto desde la raíz del proyecto.")
            return

        server_process = subprocess.Popen([python_exe, 'app.py'], cwd=cwd)
        print("      Servidor iniciado (PID: {}). Esperando 5 segundos...".format(server_process.pid))
        time.sleep(5)
    except Exception as e:
        print(f"Error fatal al iniciar servidor: {e}")
        return

    # 2. Ejecutar Script de Prueba
    print("\n[2/3] Ejecutando script de prueba (backend/test_api.py)...")
    try:
        # Ejecutamos el script de test y esperamos que termine
        result = subprocess.run([python_exe, 'test_api.py'], cwd=cwd, capture_output=True, text=True)
        
        print("\n--- SALIDA DEL TEST ---")
        print(result.stdout)
        
        if result.returncode == 0:
            print("[EXITOSO] La prueba finalizó correctamente.")
        else:
            print("[FALLIDO] El script de prueba falló.")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"Error al ejecutar test: {e}")
    finally:
        # 3. Cerrar Servidor
        print("\n[3/3] Deteniendo servidor...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("      Servidor detenido.")
        
    print("\n" + "="*60)
    print("      PRUEBA FINALIZADA")
    print("="*60)
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
