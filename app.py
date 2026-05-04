from flask import Flask, request
import urllib.parse
from datetime import datetime

app = Flask(__name__)

# ====== PRICING (EDIT HERE ONLY) ======
PRICES = {
    "single_hinge": 2500,
    "double_hinge": 4500,
    "sliding_door": 3800,
    "window": 1800
}

COLOUR_MULTIPLIER = {
    "White": 1.0,
    "Black": 1.15,
    "Charcoal": 1.2,
    "Bronze": 1.25
}

# ====== HTML ======
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ACD Estimator</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial; background: #f4f6f8; margin: 0; }
.container { max-width: 420px; margin: 30px auto; background: white; padding: 20px; border-radius: 10px; }
h2 { text-align: center; }
input, select { width: 100%; padding: 10px; margin: 8px 0; }
button { width: 100%; padding: 12px; background: green; color: white; border: none; }
.logo { display:block; margin: 0 auto 15px; width:150px; }
</style>
</head>

<body>
<div class="container">

<img src="/static/logo.jpg" class="logo">

<h2>ACD Estimator</h2>

<form method="POST">

<label>Product</label>
<select name="product">
<option value="single_hinge">Single Hinge Door</option>
<option value="double_hinge">Double Hinge Door</option>
<option value="sliding_door">Sliding Door</option>
<option value="window">Window</option>
</select>

<label>Colour</label>
<select name="colour">
<option>White</option>
<option>Black</option>
<option>Charcoal</option>
<option>Bronze</option>
</select>

<label>Width (mm)</label>
<input name="width" required>

<label>Height (mm)</label>
<input name="height" required>

<label>Qty</label>
<input name="qty" value="1">

<label>Name</label>
<input name="name" required>

<label>Phone</label>
<input name="phone" required>

<label>Area</label>
<input name="area">

<button type="submit">Get Estimate</button>

</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        product = request.form["product"]
        colour = request.form["colour"]
        width = float(request.form["width"]) / 1000
        height = float(request.form["height"]) / 1000
        qty = int(request.form["qty"])

        base_price = PRICES[product]
        multiplier = COLOUR_MULTIPLIER[colour]

        sqm = width * height
        total = sqm * base_price * multiplier * qty

        name = request.form["name"]
        phone = request.form["phone"]
        area = request.form["area"]

        message = f"""
NEW QUOTE REQUEST

Name: {name}
Phone: {phone}
Area: {area}

Product: {product}
Colour: {colour}
Size: {width}m x {height}m
Qty: {qty}

Estimate: R{round(total,2)}
"""

        whatsapp_url = "https://wa.me/27791532379?text=" + urllib.parse.quote(message)

        return f'<script>window.location.href="{whatsapp_url}"</script>'

    return HTML

if __name__ == "__main__":
    app.run()
