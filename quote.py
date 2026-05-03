items = []

print("=== QUOTE SYSTEM ===")

while True:
    print("\nAdd Item")

    item = input("Item (Door/Window): ")
    desc = input("Description (e.g. Folding 3L, Sliding, Single Hinge): ")
    colour = input("Colour: ")

    width = float(input("Width (m): "))
    height = float(input("Height (m): "))
    qty = int(input("Quantity: "))

    sqm = width * height

    # Pricing rules (you can adjust these later)
    if "folding" in desc.lower():
        price_per_sqm = 2800
    elif "sliding" in desc.lower():
        price_per_sqm = 1800
    elif "hinge" in desc.lower():
        price_per_sqm = 2200
    else:
        price_per_sqm = 1500

    price = sqm * price_per_sqm * qty

    items.append({
        "item": item,
        "desc": desc,
        "colour": colour,
        "size": f"{width} x {height}",
        "qty": qty,
        "price": price
    })

    more = input("Add another item? (y/n): ")
    if more.lower() != "y":
        break

# --- CALCULATIONS ---
subtotal = sum(i["price"] for i in items)
vat = subtotal * 0.15
total = subtotal + vat

# --- OUTPUT ---
print("\n=== QUOTE ===")
print("{:<10} {:<20} {:<10} {:<10} {:<5} {:<10}".format(
    "Item", "Description", "Colour", "Size", "Qty", "Price"))

for i in items:
    print("{:<10} {:<20} {:<10} {:<10} {:<5} R {:.2f}".format(
        i["item"], i["desc"], i["colour"], i["size"], i["qty"], i["price"]))

print("\nSubtotal: R {:.2f}".format(subtotal))
print("VAT (15%): R {:.2f}".format(vat))
print("TOTAL: R {:.2f}".format(total))
