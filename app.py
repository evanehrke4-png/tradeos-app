from flask import Flask, request, render_template_string
import urllib.parse
import os
from datetime import datetime

app = Flask(__name__)

def generate_ref():
    file = "ref.txt"
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("1")

    with open(file, "r") as f:
        number = int(f.read())

    with open(file, "w") as f:
        f.write(str(number + 1))

    return f"ACD-Q-{datetime.now().year}-{str(number).zfill(4)}

def save_lead(data):
    with open("leads.txt", "a") as f:
        f.write(data + "\n" + "-"*50 + "\n")

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
}
h2 {
  text-align: center;
}
label {
  display: block;
  font-weight: bold;
  margin-top: 10px;
}
select, input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  width: 100%;
  padding: 14px;
  margin-top: 15px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
}
.add-btn {
  background: #2980b9;
  color: white;
}
.submit-btn {
  background: #27ae60;
  color: white;
}
.item {
  border: 1px solid #ddd;
  padding: 12px;
  margin-top: 10px;
  border-radius: 8px;
}
.result {
  background: #eafaf1;
  padding: 15px;
  margin-top: 15px;
  border-radius: 8px;
  text-align: center;
}
</style>

<script>
function addItem() {
  let container = document.getElementById("items");

  let block = document.createElement("div");
  block.className = "item";

  block.innerHTML = `
    <label>Product Type</label>
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

    <label>Aluminium Colour</label>
    <select name="colour">
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

<label>Product Type</label>
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

<label>Aluminium Colour</label>
<select name="colour">
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

</div>
</div>

<button type="button" class="add-btn" onclick="addItem()">+ Add Another Item</button>

<label>Your Name</label>
<input name="name" required>

<label>Phone Number</label>
<input name="phone" required>

<label>Your Area</label>
<input name="area">

<button type="submit" class="submit-btn">Get Estimate</button>

</form>

{% if total_low %}
<div class="result">
<strong>Estimated Price Range</strong><br>
R{{total_low}} - R{{total_high}}

<br><br>

<a href="{{whatsapp}}" target="_blank">Send via WhatsApp</a>
</div>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    total_low = total_high = 0
    whatsapp = ""

    if request.method == "POST":

        products = request.form.getlist("product")
        widths = request.form.getlist("width")
        heights = request.form.getlist("height")
        qtys = request.form.getlist("qty")
        colours = request.form.getlist("colour")

        ref = generate_ref()
        now = datetime.now()
        date = now.strftime("%d %B %Y")
        time = now.strftime("%H:%M")

        items_text = ""

        for i in range(len(products)):
            width = float(widths[i]) / 1000
            height = float(heights[i]) / 1000
            qty = int(qtys[i])
            product = products[i]
            colour = colours[i]

            area = width * height * qty

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
            else:
                rate = 1800

            if colour in ["Black", "Charcoal"]:
                rate += 500
            elif colour == "Bronze":
                rate += 300
            elif colour == "Natural":
                rate -= 100

            low = int(area * rate * 0.9)
            high = int(area * rate * 1.1)

            total_low += low
            total_high += high

            items_text += f"{product} ({colour}) - R{low} to R{high}\\n"

        msg = f"""*ACD ESTIMATOR REQUEST*

REF: {ref}
DATE: {date}
TIME: {time}

*Client Details*
Name: {request.form['name']}
Phone: {request.form['phone']}
Area: {request.form['area']}

*Items*
{items_text}

*TOTAL*
R{total_low} - R{total_high}
"""

        whatsapp = "https://wa.me/27791532379?text=" + urllib.parse.quote(msg)

        save_lead(msg)

    return render_template_string(HTML, total_low=total_low, total_high=total_high, whatsapp=whatsapp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
