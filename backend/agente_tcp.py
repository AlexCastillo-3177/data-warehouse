"""
Agente TCP — Simula un sistema transaccional
Lee el CSV de órdenes y envía cada registro al servidor
"""

import socket
import time
import csv
import os

HOST = '127.0.0.1'
PORT = 12000
ARCHIVO_CSV = os.path.join('..', 'datos', 'olist_orders_dataset.csv')
MAX_REGISTROS = 30   

def enviar_datos():
    print(f"[TCP AGENTE] Conectando a {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"[TCP AGENTE] Conectado")
        except ConnectionRefusedError:
            print("[TCP AGENTE] No se pudo conectar. ¿Está el servidor activo?")
            return

        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            encabezado = next(reader)          
            print(f"[TCP AGENTE] Columnas: {encabezado}")
            print(f"[TCP AGENTE] Enviando {MAX_REGISTROS} registros...\n")

            for i, fila in enumerate(reader):
                if i >= MAX_REGISTROS:
                    break

                mensaje = ','.join(fila)
                s.send(mensaje.encode('utf-8'))
                print(f"  → Registro {i+1}/{MAX_REGISTROS}: {mensaje[:70]}...")
                time.sleep(1)   

    print(f"\n[TCP AGENTE] Envío completado. {MAX_REGISTROS} registros enviados.")

if __name__ == '__main__':
    enviar_datos()