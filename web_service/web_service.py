from flask import Flask, render_template_string, request, redirect
import requests
import time

app = Flask(__name__)

# ÖNEMLİ: Kendi en güncel API adresinizi buraya yazın
API_URL = "https://hello-cloud3-37.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
    <title>Ziyaretçi Defteri</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #f4f7f6; }
        .container { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        input { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; border-radius: 5px; }
        ul { list-style: none; padding: 0; margin-top: 20px; text-align: left; }
        li { padding: 8px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ziyaretçi Defteri</h1>
        <form method="POST">
            <input type="text" name="isim" placeholder="Adınız" required>
            <input type="text" name="sehir" placeholder="Şehriniz" required>
            <button type="submit">Gönder</button>
        </form>
        <h3>Son Ziyaretçiler:</h3>
        <ul>
            {% for z in isimler %}
                <li><strong>{{ z.isim }}</strong> - {{ z.sehir }}</li>
            {% else %}
                <li>Henüz kimse yazmadı.</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        sehir = request.form.get("sehir")
        if isim and sehir:
            try:
                # Veriyi gönder
                requests.post(f"{API_URL}/ziyaretciler", json={"isim": isim, "sehir": sehir}, timeout=10)
                # Veritabanına yazılması için çok kısa bir bekleme (Render yavaşlığı için)
                time.sleep(0.5)
            except:
                pass
        return redirect("/")

    # Verileri çekme işlemi
    isimler = []
    try:
        resp = requests.get(f"{API_URL}/ziyaretciler", timeout=10)
        if resp.status_code == 200:
            isimler = resp.json()
    except Exception as e:
        print(f"Veri çekme hatası: {e}")

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
