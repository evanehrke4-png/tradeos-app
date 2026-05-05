from flask import Flask, request, render_template_string
import urllib.parse
import os
from datetime import datetime

app = Flask(__name__)

# ===== GENERATE PROFESSIONAL REFERENCE =====
def generate_ref():
    file = "ref.txt"
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("1")

    with open(file, "r") as f:
        number = int(f.read())

    new_number = number + 1

    with open(file, "w") as f:
        f.write(str(new_number))

    year = datetime.now().year
    return f"Q-{year}-{str(number).zfill(4)}"

# ===== SAVE LEAD =====
def save_lead(data):
    with open("leads.txt", "a") as f:
        f.write(data + "\n" + "-"*40 + "\n")

# ===== HTML =====
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ACD Estimator</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
  font-family: Arial;
  background: #f4f6f8;
  margin: 0;
}
.container {
  max-width: 420px;
  margin: 30px auto;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.logo {
  display: block;
  margin: 0 auto 10px;
  max-width: 140px;
}
h2 {
  text-align: center;
  margin-bottom: 5px;
}
.company {
  text-align: center;
  font-size: 13px;
  color: #555;
  margin-bottom: 15px;
}
label {
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
  display: block;
}
select, input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}
button {
  width: 100%;
  padding: 14px;
  background: #2ecc71;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 6px;
  margin-top: 15px;
  font-weight: bold;
}
.result {
  background: #eafaf1;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
  text-align: center;
}
.whatsapp {
  display: block;
  margin-top: 10px;
  color: #25D366;
  font-weight: bold;
  text-decoration: none;
}
.disclaimer {
  font-size: 12px;
  color: #666;
  margin-top: 10px;
}
.footer {
  text-align: center;
  font-size: 12px;
  color: #888;
  margin-top: 20px;
}
</style>
</head>

<body>

<div class="container">

<img src="/static/logo.png" class="logo">

<h2>ACD Estimator</h2>
<div class="company">Aluminium & Container Dynamics (Pty) Ltd</div>

<form method="POST">

<label>Product Type</label>
<select name="product" required>
  <option>Single Hinge Door</option>
  <option>Double Hinge Door</option>
  <option>Sliding Door</option>
  <option>Pivot Door</option>
  <option>Folding Door (3 Leaf)</option>
  <option>Folding Door (5 Leaf)</option>
  <option>Folding Door (7 Leaf)</option>
  <option>Top Hung Window</option>
  <option>Side Hung Window</option>
  <option>Sliding Window</option>
  <option>Stacking Window</option>
  <option>Fixed Panel / Shopfront</option>
</select>

<label>Aluminium Colour</label>
<select name="colour" required>
  <option>White</option>
  <option>Bronze</option>
  <option>Black</option>
  <option>Charcoal</option>
  <option>Natural</option>
</select>

<label>Width (mm)</label>
<input type="number" name="width" required>

<label>Height (mm)</label>
<input type="number" name="height" required>

<label>Quantity</label>
<input type="number" name="qty" value="1" required>

<label>Your Name</label>
<input name="name" required>

<label>Phone Number</label>
<input name="phone" required>

<label>Your Area</label>
<input name="area">

<button type="submit">Get Estimate</button>
</form>

{% if price_low %}
<div class="result">
<strong>Estimated Price Range</strong><br>
R{{price_low}} - R{{price_high}}

<div class="disclaimer">
Estimate only. Final pricing after site inspection.
</div>

<a class="whatsapp" href="{{whatsapp}}" target="_blank">
Send via WhatsApp
</a>
</div>
{% endif %}

<div class="footer">
Powered by ACD Estimator
</div>

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    price_low = price_high = None
    whatsapp = ""

    if request.method == "POST":
        width = float(request.form["width"]) / 1000
        height = float(request.form["height"]) / 1000
        qty = int(request.form["qty"])

        area = width * height * qty
        product = request.form["product"]

        pricing = {
            "Single Hinge Door": (3200, 4200),
            "Double Hinge Door": (3600, 4000),
            "Sliding Door": (2800, 3800),
            "Pivot Door": (3400, 4200),
            "Folding Door (3 Leaf)": (2800, 3600),
            "Folding Door (5 Leaf)": (2800, 3800),
            "Folding Door (7 Leaf)": (2900, 3900),
            "Top Hung Window": (1400, 3000),
            "Side Hung Window": (1800, 2600),
            "Sliding Window": (1700, 2600),
            "Stacking Window": (3000, 4500),
            "Fixed Panel / Shopfront": (3000, 4500)
        }

        min_rate, max_rate = pricing.get(product, (2000, 3000))

        colour = request.form["colour"]

        price_low = area * min_rate
        price_high = area * max_rate

        if colour == "Natural":
            price_low *= 1.15
            price_high *= 1.15

        price_low = int(price_low)
        price_high = int(price_high)

        ref = generate_ref()
        now = datetime.now()
        date = now.strftime("%d %B %Y")
        time = now.strftime("%H:%M")

        msg = f"""*ACD ESTIMATOR REQUEST*

REF: {ref}
DATE: {date}
TIME: {time}

Name: {request.form['name']}
Phone: {request.form['phone']}
Area: {request.form['area']}

Product: {product}
Size: {request.form['width']} x {request.form['height']} mm
Colour: {colour}
Qty: {qty}

Estimate:
R{price_low} - R{price_high}
"""

        whatsapp = "https://wa.me/27791532379?text=" + urllib.parse.quote(msg)

        save_lead(msg)

    return render_template_string(HTML, price_low=price_low, price_high=price_high, whatsapp=whatsapp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
