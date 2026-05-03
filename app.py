from flask import Flask, request, render_template_string
import urllib.parse
import os
from datetime import datetime
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>TradeOS Instant Quote</title>
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
h2 {
  text-align: center;
  margin-bottom: 20px;
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
</style>
</head>

<body>

<div class="container">
<h2>TradeOS Instant Quote</h2>

<form method="POST">

<label>Product Type</label>
<select name="product" required>
  <optgroup label="Doors">
    <option value="Single Hinge Door">Single Hinge Door</option>
    <option value="Double Hinge Door">Double Hinge Door</option>
    <option value="Sliding Door">Sliding Door</option>
    <option value="Pivot Door">Pivot Door</option>
    <option value="Folding Door (3 Leaf)">Folding Door (3 Leaf)</option>
    <option value="Folding Door (5 Leaf)">Folding Door (5 Leaf)</option>
    <option value="Folding Door (7 Leaf)">Folding Door (7 Leaf)</option>
  </optgroup>

  <optgroup label="Windows">
    <option value="Top Hung Window">Top Hung Window</option>
    <option value="Side Hung Window">Side Hung Window</option>
    <option value="Sliding Window">Sliding Window</option>
    <option value="Stacking Window">Stacking Window</option>
    <option value="Fixed Panel / Shopfront">Fixed Panel / Shopfront</option>
  </optgroup>
</select>

<label>Aluminium Colour</label>
<select name="colour" required>
  <option value="White">White</option>
  <option value="Bronze">Bronze</option>
  <option value="Black">Black</option>
  <option value="Charcoal">Charcoal</option>
  <option value="Natural">Natural (Mill Finish)</option>
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
Please note: This is an estimated price only. Final pricing may vary after a site inspection.
Installation, delivery, and additional materials are not included.
</div>

<a class="whatsapp" href="{{whatsapp}}" target="_blank">
Send via WhatsApp
</a>
</div>
{% endif %}

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

        # Pricing logic
        if "Single Hinge" in product:
            rate = 3200
        elif "Double Hinge" in product:
            rate = 4200
        elif "Sliding Door" in product:
            rate = 3800
        elif "Pivot" in product:
            rate = 6500
        elif "3 Leaf" in product:
            rate = 7500
        elif "5 Leaf" in product:
            rate = 9000
        elif "7 Leaf" in product:
            rate = 10500
        elif "Sliding Window" in product:
            rate = 2200
        elif "Stacking Window" in product:
            rate = 3000
        elif "Fixed" in product:
            rate = 1800
        else:
            rate = 1800

        # Colour adjustments
        colour = request.form["colour"]
        if colour in ["Black", "Charcoal"]:
            rate += 500
        elif colour == "Bronze":
            rate += 300
        elif colour == "Natural":
            rate -= 100

        price_low = int(area * rate * 0.9)
        price_high = int(area * rate * 1.1)

        # Reference + Date + Time
        ref = f"Q{random.randint(1000,9999)}"
        now = datetime.now()
        date = now.strftime("%d %B %Y")
        time = now.strftime("%H:%M")

        msg = f"""*TRADEOS QUOTE REQUEST*

Ref: {ref}
Date: {date}
Time: {time}

*Client Details*
Name: {request.form['name']}
Phone: {request.form['phone']}
Area: {request.form['area']}

*Project Details*
Product: {product}
Size: {request.form['width']}mm x {request.form['height']}mm
Colour: {colour}
Quantity: {qty}

*Estimated Price Range*
R{price_low} - R{price_high}

*Important Note*
This is a preliminary estimate based on the information provided.
Final pricing may vary after a site inspection and detailed quotation.
Installation, delivery, and additional materials are not included.
"""

        whatsapp = "https://wa.me/27791532379?text=" + urllib.parse.quote(msg)

    return render_template_string(HTML, price_low=price_low, price_high=price_high, whatsapp=whatsapp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
