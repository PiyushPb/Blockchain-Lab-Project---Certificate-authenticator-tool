import hashlib
import base64
from flask import Flask, request, render_template
app = Flask(__name__)

certificates = {}

def generate_token(certificate_data):
    sha256 = hashlib.sha256()
    sha256.update(certificate_data)
    return sha256.hexdigest()

@app.route('/upload', methods=['GET', 'POST'])
def upload_certificate():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            certificate_data = file.read()
            token = generate_token(certificate_data)
            certificates[token] = certificate_data
            return f"Certificate uploaded successfully! Token: {token}"

    return render_template('index.html')

@app.route('/display/<token>', methods=['GET'])
def display_certificate(token):
    certificate_data = certificates.get(token)
    if certificate_data:
        certificate_base64 = base64.b64encode(certificate_data).decode()
        return render_template('display.html', certificate=certificate_base64)
    else:
        return "Certificate not found"

if __name__ == '__main__':
    app.run(debug=True)
