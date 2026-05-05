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

    new_number = number + 1

    with open(file, "w") as f:
        f.write(str(new_number))

    year = datetime.now().year
    return f"Q-{year}-{str(number).zfill(4)}"

def save_lead(data):
    with open("leads.txt", "a") as f:
        f.write(data + "\n" + "-"*40 + "\n")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ACD Estimator</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body { font-family: Arial; background: #f4f6f8; margin: 0; }
.container { max-width: 420px; margin: 30px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.logo { display: block; margin: 0 auto 10px; max-width: 140px; }
h2 { text-align: center; margin-bottom: 5px; }
.company { text-align: center; font-size: 13px; color: #555; margin-bottom: 15px; }
label { font-size: 14px; font-weight: bold; margin-top: 10px; display: block; }
select, input { width: 100%; padding: 12px; margin-top: 5px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; }
button { width: 100%; padding: 14px; background: #2ecc71; border: none; color: white; font-size: 16px; border-radius: 6px; margin-top: 15px; font-weight: bold; }
.add-btn { background: #3498db; margin-top: 10px; }
.result { background: #eafaf1; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; }
.whatsapp { display: block; margin-top: 10px; color: #25D366; font-weight: bold; text-decoration: none; }
.disclaimer { font-size: 12px; color: #666; margin-top: 10px; text-align:left; }
.footer { text-align: center; font-size: 12px; color: #888; margin-top: 20px; }
</style>

<script>
function addItem() {
    const container = document.getElementById("items");
    const item = container.children[0].cloneNode(true);
    container.appendChild(item);
}
</script>

</head>

<body>

<div class="container">

<img src="/static/logo.png" class="logo">

<h2>ACD Estimator</h2>
<div class="company">Aluminium & Container Dynamics (Pty) Ltd</div>

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
<input type="number" name="width">

<label>Height (mm)</label>
<input type="number" name="height">

<label>Quantity</label>
<input type="number" name="qty" value="1">

<hr>

</div>
</div>

<button type="button" class="add-btn" onclick="addItem()">+ Add Another Item</button>

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

<strong>Item Breakdown</strong><br><br>
{{ breakdown|safe }}

<strong>Total Estimate</strong><br>
R{{price_low}} - R{{price_high}}

<div class="disclaimer">
<strong>Please Note:</strong>
<ul style="padding-left:18px;">
<li>Prices include manufacturing, standard installation, and delivery within a 50km radius of Johannesburg.</li>
<li>Estimates include one site inspection and final measurements.</li>
<li>All prices exclude 15% VAT.</li>
<li>Estimates are based on standard specifications and provide a reliable indication of final project cost.</li>
<li>For urgent requests or a detailed quotation breakdown, please send your estimate via WhatsApp.</li>
</ul>
</div>

<a class="whatsapp" href="{{whatsapp}}" target="_blank">
Send via WhatsApp
</a>

</div>
{% endif %}

<div class="footer">Powered by ACD Estimator</div>

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    price_low = price_high = 0
    whatsapp = ""
    breakdown_html = ""

    if request.method == "POST":

        products = request.form.getlist("product")
        colours = request.form.getlist("colour")
        widths = request.form.getlist("width")
        heights = request.form.getlist("height")
        qtys = request.form.getlist("qty")

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

        details = ""

        for i in range(len(products)):
            if widths[i] and heights[i]:
                w = float(widths[i]) / 1000
                h = float(heights[i]) / 1000
                q = int(qtys[i]) if qtys[i] else 1

                area = w * h * q
                min_rate, max_rate = pricing.get(products[i], (2000, 3000))

                low = area * min_rate
                high = area * max_rate

                if colours[i] == "Natural":
                    low *= 1.15
                    high *= 1.15

                price_low += low
                price_high += high

                low_i = int(low)
                high_i = int(high)

                details += f"{products[i]} ({w}x{h}m x{q}) → R{low_i} - R{high_i}\\n"
                breakdown_html += f"<div><strong>{products[i]}</strong><br>R{low_i} - R{high_i}</div><br>"

        price_low = int(price_low)
        price_high = int(price_high)

        ref = generate_ref()

        msg = f"""*ACD ESTIMATOR REQUEST*

REF: {ref}

Name: {request.form['name']}
Phone: {request.form['phone']}
Area: {request.form['area']}

Items:
{details}

Total Estimate:
R{price_low} - R{price_high}
"""

        whatsapp = "https://wa.me/27791532379?text=" + urllib.parse.quote(msg)

        save_lead(msg)

    return render_template_string(HTML, price_low=price_low, price_high=price_high, whatsapp=whatsapp, breakdown=breakdown_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
