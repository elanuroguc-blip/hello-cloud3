from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

API_URL = "https://hello-cloud3-20.onrender.com"

HTML = """
<!doctype html>
<html>
  <head>
    <title>Mikro Hizmetli Selam!</title>
    <style>
      body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
      h1 { color: #333; }
      input { padding: 10px; font-size: 16px; margin: 5px; }
      button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
      li { background: white; margin: 5px auto; padding: 10px; border-radius: 5px; max-width: 350px; text-align: left; }
      ul { list-style-type: none; padding: 0; }
      form { margin-bottom: 20px; }
    </style>
  </head>
  <body>
    <h1>Mikro Hizmetli Selam!</h1>
    
    <form method="POST">
      <input type="text" name="isim" placeholder="Adını yaz" required>
      <input type="text" name="sehir" placeholder="Şehrini yaz" required>
      <button type="submit">Gönder</button>
    </form>
    
    <h3>Ziyaretçiler ve Şehirleri:</h3>
    <ul>
      {% for ziyaretci in isimler %}
        <li>{{ ziyaretci.isim }} - ({{ ziyaretci.sehir }})</li>
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

        gonderilecek_veri = {"isim": isim, "sehir": sehir}

        requests.post(API_URL + "/ziyaretciler", json=gonderilecek_veri)
        return redirect("/")

    resp = requests.get(API_URL + "/ziyaretciler")
    isimler = []
    if resp.status_code == 200:
        isimler = resp.json()

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
