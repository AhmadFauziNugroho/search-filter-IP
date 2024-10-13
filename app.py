from flask import Flask, render_template, request
import re
import requests

app = Flask(__name__)

# Halaman utama untuk mengunggah file
@app.route('/')
def upload_file():
    return render_template('upload.html')

# Route untuk mengekstrak IP dan mendeteksi informasi lokasi
@app.route('/detect', methods=['POST'])
def detect_ip():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Baca file log dan ekstrak IP
    log_data = file.read().decode()
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ips = ip_pattern.findall(log_data)
    
    ip_info = []
    
    # Mengambil informasi geolokasi untuk setiap IP
    for ip in sorted(set(ips)):  # Hapus duplikat dan urutkan
        if ip:
            response = requests.get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            ip_info.append({
                'ip': ip,
                'country': data.get('country'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'isp': data.get('isp')
            })
    
    # Render halaman hasil dengan informasi IP
    return render_template('result.html', ip_info=ip_info)

if __name__ == '__main__':
    app.run(debug=True)
