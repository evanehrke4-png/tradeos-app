from flask import Flask, request, render_template_string
import urllib.parse
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# 🔥 PRICING CONTROL PANEL
# =========================
PRICES = {
    "Single Hinge Door": 3200,
    "Double Hinge Door": 4200,
    "Sliding Door": 3800,
    "Pivot Door": 6500,
    "Folding Door (3 Leaf)": 7500,
    "Folding Door (5 Leaf)": 9000,
    "Folding Door (7 Leaf)": 10500,
    "Top Hung Window": 1800,
    "Side Hung Window": 1800,
    "Sliding Window": 2200,
    "Stacking Window": 3000,
    "Fixed Panel / Shopfront": 1800
}

COLOUR_EXTRA = {
    "White": 0,
    "Black": 500,
    "Charcoal": 500,
    "Bronze": 300,
    "Natural": -100
}

# =========================
# REF SYSTEM
# =========================
def generate_ref():
    file = "ref.txt"
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("1")

    with open(file, "r") as f:
        number = int(f.read())

    with open(file, "w") as f:
        f.write(str(number + 1))

    return f"ACD-Q-{datetime.now().year}-{str(number).zfill(4)}"

# =========================
# SAVE LEADS
# =========================
def save_lead(data):
    with open("leads.txt", "a") as f:
        f.write(data + "\n" + "-"*50 + "\n")

# =========================
# HTML
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ACD Estimator</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family: Arial; background: #f4f6f8; }
.container { max-width: 420px; margin: 30px auto; background: white; padding: 20px; border-radius: 10px; }
h2 { text-align: center; }
label { font-weight: bold; display:block; margin-top:10px; }
input, select { width:100%; padding:12px; margin-top:5px; border-radius:6px; border:1px solid #ccc; }
button { width:100%; padding:14px; margin-top:15px; border:none; border-radius:6px; font-weight:bold; }
.add-btn { background:#2980b9; color:white; }
.submit-btn { background:#27ae60; color:white; }
.item { border:1px solid #ddd; padding:12px; margin-top:10px; border-radius:8px; }
.result { background:#eafaf1; padding:15px; margin-top:15px; border-radius:8px; text-align:center; }
</style>

<script>
function addItem(){
  let container = document.getElementById("items");
  let block = document.createElement("div");
  block.className = "item";

  block.innerHTML = `
    <label>Product</label>
    <select name="product">
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

    <label>Colour</label>
    <select name="colour">
      <option>White</option>
      <option>Black</option>
      <option>Charcoal</option>
      <option>Bronze</option>
      <option>Natural</option>
    </select>

    <label>Width (mm)</label>
    <input type="number" name="width" required>

    <label>Height (mm)</label>
    <input type="number" name="height" required>

    <label>Qty</label>
    <input type="number" name="qty" value="1" required>
  `;

  container.appendChild(block);
}
</script>
</head>

<body>
<div class="container">
<h2>ACD Estimator</h2>

<form method="POST">

<div id="items">
<div class="item">

<label>Product</label>
<select name="product">
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

<label>Colour</label>
<select name="colour">
  <option>White</option>
  <option>Black</option>
  <option>Charcoal</option>
  <option>Bronze</option>
  <option>Natural</option>
</select>

<label>Width</label>
<input name="width" type="number" required>

<label>Height</label>
<input name="height" type="number" required>

<label>Qty</label>
<input name="qty" type="number" value="1" required>

</div>
</div>

<button type="button" class="add-btn" onclick="addItem()">+ Add Another Item</button>

<label>Name</label>
<input name="name" required>

<label>Phone</label>
<input name="phone" required>

<label>Area</label>
<input name="area">

<button type="submit" class="submit-btn">Get Estimate</button>

</form>

{% if total_low %}
<div class="result">
<strong>R{{total_low}} - R{{total_high}}</strong><br><br>
<a href="{{whatsapp}}" target="_blank">Send via WhatsApp</a>
</div>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    total_low = 0
    total_high = 0
    whatsapp = ""

    if request.method == "POST":
        products = request.form.getlist("product")
        widths = request.form.getlist("width")
        heights = request.form.getlist("height")
        qtys = request.form.getlist("qty")
        colours = request.form.getlist("colour")

        ref = generate_ref()
        items_text = ""

        for i in range(len(products)):
            product = products[i]
            width = float(widths[i]) / 1000
            height = float(heights[i]) / 1000
            qty = int(qtys[i])
            colour = colours[i]

            area = width * height * qty

            rate = PRICES.get(product, 2000)
            rate += COLOUR_EXTRA.get(colour, 0)

            low = int(area * rate * 0.9)
            high = int(area * rate * 1.1)

            total_low += low
            total_high += high

            items_text += f"{product} ({colour}) - R{low} to R{high}\\n"

        msg = f"ACD QUOTE\\nREF: {ref}\\n\\n{items_text}\\nTOTAL: R{total_low} - R{total_high}"
        whatsapp = "https://wa.me/27791532379?text=" + urllib.parse.quote(msg)

        save_lead(msg)

    return render_template_string(HTML, total_low=total_low, total_high=total_high, whatsapp=whatsapp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
