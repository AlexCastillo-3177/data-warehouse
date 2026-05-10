"""
API Flask — Expone los datos de Supabase mediante HTTP
Endpoint principal: GET /api/datos
"""

from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    "postgresql://postgres.ondamnacltotugpyjuut:YuqiSong2026@aws-1-us-west-1.pooler.supabase.com:6543/postgres"
)

def conectar():
    return psycopg2.connect(DATABASE_URL)


@app.route('/api/datos')
def get_datos():
    """Devuelve los últimos 200 registros ingresados."""
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, origen, contenido, fecha
            FROM datos_ingesta
            ORDER BY fecha DESC
            LIMIT 200
        """)
        filas = cur.fetchall()
        cur.close()
        conn.close()

        resultado = [
            {
                "id":       f[0],
                "origen":   f[1],
                "contenido": f[2],
                "fecha":    str(f[3])
            }
            for f in filas
        ]
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/estadisticas')
def get_estadisticas():
    """Devuelve el conteo de registros por origen (TCP/UDP)."""
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT origen, COUNT(*) AS total
            FROM datos_ingesta
            GROUP BY origen
            ORDER BY total DESC
        """)
        filas = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify([{"origen": f[0], "total": f[1]} for f in filas])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/por-hora')
def get_por_hora():
    """Devuelve registros agrupados por hora del día."""
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                EXTRACT(HOUR FROM fecha) AS hora,
                COUNT(*) AS total
            FROM datos_ingesta
            GROUP BY hora
            ORDER BY hora
        """)
        filas = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify([{"hora": int(f[0]), "total": f[1]} for f in filas])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("API Flask corriendo en http://localhost:5000")
    app.run(debug=True, port=5000)