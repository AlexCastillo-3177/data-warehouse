"""
Agente UDP — Simula sensores de telemetría en tiempo real
Genera datos aleatorios y los envía al servidor
"""

import socket
import time
import random
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12001
TOTAL_LECTURAS = 20   

def generar_lectura_sensor():
    """Genera datos simulados de un sensor."""
    return {
        "sensor_id":     f"SENSOR_{random.randint(1, 10):02d}",
        "temperatura":   round(random.uniform(18.0, 42.0), 2),
        "humedad":       round(random.uniform(35.0, 95.0), 2),
        "velocidad_red": round(random.uniform(1.0, 100.0), 2),
        "estado_orden":  random.choice(["delivered", "shipped", "processing", "canceled"]),
        "region":        random.choice(["SP", "RJ", "MG", "BA", "RS", "PR"]),
        "timestamp":     datetime.now().isoformat()
    }

def enviar_telemetria():
    print(f"[UDP AGENTE] Iniciando envío de telemetría a {HOST}:{PORT}")
    print(f"[UDP AGENTE] Se enviarán {TOTAL_LECTURAS} lecturas cada 0.5 segundos\n")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for i in range(TOTAL_LECTURAS):
            datos = generar_lectura_sensor()
            mensaje = json.dumps(datos)
            s.sendto(mensaje.encode('utf-8'), (HOST, PORT))
            print(f"  → Lectura {i+1}/{TOTAL_LECTURAS}: "
                  f"{datos['sensor_id']} | {datos['temperatura']}°C | "
                  f"{datos['estado_orden']}")
            time.sleep(0.5)

    print(f"\n[UDP AGENTE] Telemetría completada. {TOTAL_LECTURAS} lecturas enviadas.")

if __name__ == '__main__':
    enviar_telemetria()