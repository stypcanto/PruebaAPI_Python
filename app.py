from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# 🔑 Configuración de la conexión
DB_HOST = os.getenv("DB_HOST", "10.0.89.13")
DB_NAME = os.getenv("DB_NAME", "maestro_cenate")
DB_USER = os.getenv("DB_USER", "chatbot_cnt")   # Mejor usar usuario con permisos mínimos
DB_PASS = os.getenv("DB_PASS", "C3n3tQ123")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# 📌 Endpoint: obtener paciente por documento
@app.route("/api/pacientes/<doc>", methods=["GET"])
def get_paciente(doc):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT doc_paciente, paciente, fecnacimpaciente, sexo
            FROM asegurados
            WHERE doc_paciente = %s
            LIMIT 1;
        """, (doc,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return jsonify({
                "doc_paciente": row[0],
                "paciente": row[1],
                "fecnacimpaciente": row[2].isoformat() if row[2] else None,
                "sexo": row[3]
            })
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 Endpoint: listar primeros 20 pacientes
@app.route("/api/pacientes", methods=["GET"])
def list_pacientes():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT doc_paciente, paciente, fecnacimpaciente, sexo
            FROM asegurados
            LIMIT 20;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        pacientes = [
            {
                "doc_paciente": r[0],
                "paciente": r[1],
                "fecnacimpaciente": r[2].isoformat() if r[2] else None,
                "sexo": r[3]
            }
            for r in rows
        ]
        return jsonify(pacientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

