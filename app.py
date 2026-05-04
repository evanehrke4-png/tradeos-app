from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        area = request.form['area']
        job_type = request.form['job_type']
        details = request.form['details']

        message = f"""*NEW QUOTE REQUEST*

*Client Details*
Name: {name}
Phone: {phone}
Area: {area}

*Project*
Type: {job_type}
Details: {details}
"""

        encoded_message = urllib.parse.quote(message)

        whatsapp_url = f"https://wa.me/27791532379?text={encoded_message}"

        return f'<script>window.location.href="{whatsapp_url}"</script>'

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
