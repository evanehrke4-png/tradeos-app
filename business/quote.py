# FAST QUOTE VERSION (IMPROVED COLOUR MENU)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

styles = getSampleStyleSheet()

company_name = "Aluminium & Container Dynamics (Pty) Ltd"
logo_path = "/storage/emulated/0/Download/logo (1).jpg"

bank_details = [
    "Capitec Bank",
    "Account Type: Business Check",
    "Account Number: 1055052437",
    "Branch Code: 470010"
]

def get_next_number(file):
    if not os.path.exists(file):
        return 1
    with open(file, "r") as f:
        return int(f.read()) + 1

def save_number(file, num):
    with open(file, "w") as f:
        f.write(str(num))

print("1 Quote  2 Invoice")
doc_choice = input("Select: ")

if doc_choice == "1":
    doc_name = "Quote"
    num_file = "quote_no.txt"
    prefix = "Q"
else:
    doc_name = "Invoice"
    num_file = "invoice_no.txt"
    prefix = "INV"

number = get_next_number(num_file)
save_number(num_file, number)

number_display = f"{prefix}{str(number).zfill(4)}"

client = input("Client: ")
phone = input("Phone: ")
safe_client = client.replace(" ", "_")

date = datetime.now().strftime("%Y-%m-%d")

items = []

while True:
    print("\n1 Window 2 Single 3 Double 4 Pivot 5 Sliding 6 Folding")
    c = input("Type: ")

    types = {
        "1": ("Window",1500),
        "2": ("Door - Single",2200),
        "3": ("Door - Double",2500),
        "4": ("Door - Pivot",3000),
        "5": ("Door - Sliding",1800)
    }

    if c in types:
        desc, rate = types[c]
        item_type = "Window" if c=="1" else "Door"
    elif c == "6":
        leaves = input("Leaves: ")
        desc = f"Door - Folding ({leaves}L)"
        rate = 2800
        item_type = "Door"
    else:
        continue

    w = float(input("Width: "))
    h = float(input("Height: "))
    q = int(input("Qty: "))

    # --- CLEAN COLOUR MENU ---
    print("\nSelect Colour:")
    print("1. Bronze")
    print("2. Black")
    print("3. White")
    print("4. Charcoal")
    print("5. Natural")

    colour_choice = input("Enter number: ")

    colour_map = {
        "1": "Bronze",
        "2": "Black",
        "3": "White",
        "4": "Charcoal",
        "5": "Natural"
    }

    colour = colour_map.get(colour_choice, "Bronze")

    sqm = w*h
    price = sqm*rate*q

    if price < 3500:
        price = 3500

    items.append([item_type, desc, colour, f"{w}x{h}", q, f"R {price:.2f}"])

    if input("Add more? (y/n): ") != "y":
        break

subtotal = sum(float(i[5].replace("R ","")) for i in items)
vat = subtotal * 0.15
total = subtotal + vat

file_name = f"/storage/emulated/0/Download/{company_name} {doc_name} {number_display} {safe_client}.pdf"

doc = SimpleDocTemplate(file_name, pagesize=A4)
elements = []

logo = Image(logo_path, width=480, height=110)
logo.hAlign='CENTER'
elements.append(logo)
elements.append(Spacer(1,10))

elements.append(Paragraph(f"<b>{company_name}</b>", styles["Normal"]))
elements.append(Paragraph(f"{doc_name} No: {number_display}", styles["Normal"]))
elements.append(Paragraph(f"Date: {date}", styles["Normal"]))

elements.append(Spacer(1,10))

elements.append(Paragraph(f"Client: {client}", styles["Normal"]))
elements.append(Paragraph(phone, styles["Normal"]))

elements.append(Spacer(1,15))

table_data=[["Item","Description","Colour","Size","Qty","Price"]]
table_data.extend(items)

table=Table(table_data,colWidths=[60,150,80,80,40,90])
table.setStyle(TableStyle([
("BACKGROUND",(0,0),(-1,0),colors.grey),
("TEXTCOLOR",(0,0),(-1,0),colors.white),
("GRID",(0,0),(-1,-1),1,colors.black)
]))

elements.append(table)

elements.append(Spacer(1,20))

elements.append(Paragraph(f"Subtotal: R {subtotal:.2f}", styles["Normal"]))
elements.append(Paragraph(f"VAT: R {vat:.2f}", styles["Normal"]))
elements.append(Paragraph(f"<b>TOTAL: R {total:.2f}</b>", styles["Heading2"]))

elements.append(Spacer(1,20))

elements.append(Paragraph("<b>Banking Details</b>", styles["Normal"]))
for b in bank_details:
    elements.append(Paragraph(b, styles["Normal"]))

doc.build(elements)

print("Saved:",file_name)
os.system(f"termux-open '{file_name}'")
