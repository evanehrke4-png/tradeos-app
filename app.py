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
<select name="product">
  <option value="window">Window</option>
  <option value="door">Door</option>
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
        width = float(request.form["width"])
        height = float(request.form["height"])
        qty = int(request.form["qty"])
        name = request.form["name"]
        phone = request.form["phone"]
        area_loc = request.form["area"]

        # Save lead (will improve later for cloud)
        with open("leads.txt", "a") as f:
            f.write(f"{name},{phone},{product},{width}x{height},Qty:{qty},{area_loc}\\n")

        # Calculate area
        area = (width * height) / 1000000

        # Pricing
        if product == "window":
            low_rate = 1800
            high_rate = 2500
        else:
            low_rate = 2500
            high_rate = 4000

        low_price = area * low_rate * qty
        high_price = area * high_rate * qty

        result = f"Estimated: R{int(low_price)} - R{int(high_price)}"

        # WhatsApp message
        message = f"""Quote Request:
Product: {product}
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
