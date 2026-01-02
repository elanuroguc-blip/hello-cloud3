from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = "postgresql://hello_cloud3_db_5c33_user:v0zPhI7xUyBJiQXRzhSM9DOnUAT8FsJS@dpg-d3tjhd0gjchc73fan1s0-a.oregon-postgres.render.com/hello_cloud3_db_5c33?"

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Tabloyu oluştur (Eğer daha önceden hatalı oluştuysa diye kontrol eder)
        cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, sehir TEXT)")
        conn.commit()

        if request.method == "POST":
            data = request.get_json()
            if data and 'isim' in data and 'sehir' in data:
                cur.execute("INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)", (data['isim'], data['sehir']))
                conn.commit()

        # Verileri çek
        cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
        isimler = [{"isim": row[0], "sehir": row[1]} for row in cur.fetchall()]
        
        cur.close()
        return jsonify(isimler)
    
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
