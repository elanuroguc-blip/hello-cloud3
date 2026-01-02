from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# ÖNEMLİ: api_service adresinizi buraya yazın (sonunda / olmasın)
API_URL = "https://hello-cloud3-20.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
    <title>Ziyaretçi Defteri</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; margin: 5px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; max-width: 350px; margin: 20px auto; text-align: left; }
        li { background: white; margin: 5px auto; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adınızı yaz" required>
        <input type="text" name="sehir" placeholder="Şehrinizi yaz" required>
        <button type="submit">Gönder</button>
    </form>

    <h3>Ziyaretçiler ve Şehirleri:</h3>
    <ul>
        {% for ziyaretci in isimler %}
            <li>{{ ziyaretci.isim }} - {{ ziyaretci.sehir }}</li>
        {% endfor %}
    </ul>
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
                # Veriyi API'ye gönder
                requests.post(f"{API_URL}/ziyaretciler", json={"isim": isim, "sehir": sehir}, timeout=5)
            except Exception as e:
                print(f"Hata oluştu: {e}")
        
        return redirect("/")

    # Sayfa her yüklendiğinde verileri çek
    isimler = []
    try:
        resp = requests.get(f"{API_URL}/ziyaretciler", timeout=5)
        if resp.status_code == 200:
            isimler = resp.json()
    except Exception as e:
        print(f"Veri çekme hatası: {e}")

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
