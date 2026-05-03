from flask import Flask, request, render_template_string
import urllib.parse
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>TradeOS Quote</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
  font-family: Arial;
  background: #f5f5f5;
  padding: 20px;
}
.container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  margin: auto;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
h2 {
  text-align: center;
}
input, select {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}
button {
  width: 100%;
  padding: 12px;
  background: #25D366;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
}
.result {
  margin-top: 15px;
  padding: 10px;
  background: #eaffea;
  border-radius: 5px;
}
.note {
  margin-top: 10px;
  font-size: 13px;
  color: #555;
}
a {
  display: block;
  text-align: center;
  margin-top: 10px;
  color: #25D366;
  font-weight: bold;
}
</style>
</head>

<body>
<div class="container">
<h2>TradeOS Instant Quote</h2>

<form method="POST">

<select name="product" required>
  <optgroup label="Doors">
    <option value="single_hinge">Single Hinge Door</option>
    <option value="double_hinge">Double Hinge Door</option>
    <option value="sliding_door">Sliding Door</option>
    <option value="pivot_door">Pivot Door</option>
    <option value="folding_3">Folding Stacking Door (3 Leaf)</option>
    <option value="folding_5">Folding Stacking Door (5 Leaf)</option>
    <option value="folding_7">Folding Stacking Door (7 Leaf)</option>
  </optgroup>

  <optgroup label="Windows">
    <option value="top_hung">Top Hung Window</option>
    <option value="side_hung">Side Hung Window</option>
    <option value="sliding_window">Sliding Window</option>
    <option value="stacking_window">Stacking Window</option>
    <option value="fixed">Fixed Panel / Shopfront</option>
  </optgroup>
</select>

<select name="color" required>
  <option value="white">White</option>
  <option value="bronze">Bronze</option>
  <option value="black">Black</option>
  <option value="charcoal">Charcoal</option>
  <option value="natural">Natural (Mill Finish)</option>
</select>

<input type="number" name="width" placeholder="Width (mm)" required>
<input type="number" name="height" placeholder="Height (mm)" required>
<input type="number" name="qty" value="1" required>

<input type="text" name="name" placeholder="Your Name" required>
<input type="text" name="phone" placeholder="Phone Number" required>
<input type="text" name="area" placeholder="Your Area">

<button type="submit">Get Estimate</button>
</form>

{% if result %}
<div class="result">
<p>{{result}}</p>

<div class="note">
Please note: This is an estimated price based on the information provided. Final pricing may vary after a site inspection and detailed quotation. Prices exclude installation, delivery, and any additional hardware unless specified.
</div>

<a href="{{whatsapp_link}}">Send on WhatsApp</a>
</div>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        product = request.form["product"]
        color = request.form["color"]
        width = float(request.form["width"])
        height = float(request.form["height"])
        qty = int(request.form["qty"])
        name = request.form["name"]
        phone = request.form["phone"]
        area_loc = request.form["area"]

        # Save lead
        with open("leads.txt", "a") as f:
            f.write(f"{name},{phone},{product},{color},{width}x{height},Qty:{qty},{area_loc}\\n")

        area = (width * height) / 1000000

        # Pricing
        if product == "single_hinge":
            price_per_m2 = 3200
        elif product == "double_hinge":
            price_per_m2 = 4200
        elif product == "sliding_door":
            price_per_m2 = 3800
        elif product == "pivot_door":
            price_per_m2 = 6500
        elif product == "folding_3":
            price_per_m2 = 7500
        elif product == "folding_5":
            price_per_m2 = 9000
        elif product == "folding_7":
            price_per_m2 = 10500
        elif product == "top_hung":
            price_per_m2 = 1800
        elif product == "side_hung":
            price_per_m2 = 1800
        elif product == "sliding_window":
            price_per_m2 = 2200
        elif product == "stacking_window":
            price_per_m2 = 3000
        elif product == "fixed":
            price_per_m2 = 1800

        # Colour adjustments
        if color in ["black", "charcoal"]:
            price_per_m2 += 500
        elif color == "bronze":
            price_per_m2 += 300
        elif color == "natural":
            price_per_m2 -= 100

        low_price = area * price_per_m2 * qty * 0.9
        high_price = area * price_per_m2 * qty * 1.1

        result = f"Estimated: R{int(low_price)} - R{int(high_price)}"

        message = f"""Quote Request:
Product: {product}
Colour: {color}
Size: {width} x {height}
Qty: {qty}
Area: {area_loc}
Name: {name}
Phone: {phone}
"""

        link = "https://wa.me/27791532379?text=" + urllib.parse.quote(message)

        return render_template_string(HTML, result=result, whatsapp_link=link)

    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
