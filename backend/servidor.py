"""
Servidor Concurrente TCP + UDP
Recibe datos de los agentes y los almacena en Supabase
"""

import socket
import threading
import psycopg2
import json
from datetime import datetime

DATABASE_URL = "postgresql://postgres.ondamnacltotugpyjuut:YuqiSong2026@aws-1-us-west-1.pooler.supabase.com:6543/postgres"

def insertar_en_db(origen, contenido):
    """Inserta un registro en la base de datos."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO datos_ingesta (origen, contenido) VALUES (%s, %s)",
            (origen, contenido)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"  [{origen}] Guardado en DB")
    except Exception as e:
        print(f"  Error DB: {e}")


# ── SERVIDOR TCP ──────────────────────────────────────────────────────────────

def manejar_cliente_tcp(conexion, direccion):
    """Hilo que atiende a un cliente TCP específico."""
    print(f"[TCP] Nueva conexión de {direccion}")
    with conexion:
        while True:
            datos = conexion.recv(4096)
            if not datos:
                print(f"[TCP] {direccion} se desconectó")
                break
            contenido = datos.decode('utf-8')
            print(f"[TCP] Recibido de {direccion}: {contenido[:60]}...")
            insertar_en_db('TCP', contenido)

def iniciar_servidor_tcp():
    """Servidor TCP que acepta múltiples clientes con hilos."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 12000))
    s.listen(5)
    print("[TCP] Servidor escuchando en 127.0.0.1:12000 ...")
    while True:
        conexion, direccion = s.accept()
        hilo = threading.Thread(
            target=manejar_cliente_tcp,
            args=(conexion, direccion),
            daemon=True
        )
        hilo.start()


# ── SERVIDOR UDP ──────────────────────────────────────────────────────────────

def iniciar_servidor_udp():
    """Servidor UDP que recibe datagramas de telemetría."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 12001))
    print("[UDP] Servidor escuchando en 127.0.0.1:12001 ...")
    while True:
        datos, direccion = s.recvfrom(4096)
        contenido = datos.decode('utf-8')
        print(f"[UDP] Recibido de {direccion}: {contenido[:60]}...")
        insertar_en_db('UDP', contenido)


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 55)
    print("   SERVIDOR DATA WAREHOUSE — TCP:12000 | UDP:12001")
    print("=" * 55)

    hilo_tcp = threading.Thread(target=iniciar_servidor_tcp, daemon=True)
    hilo_udp = threading.Thread(target=iniciar_servidor_udp, daemon=True)

    hilo_tcp.start()
    hilo_udp.start()

    print("\n Servidor activo. Esperando agentes...")
    print("   Presiona Ctrl+C para detener.\n")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n Servidor detenido.")