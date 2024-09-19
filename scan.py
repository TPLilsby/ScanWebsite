from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
CONFIG_FILE = 'barcode_folders.txt'

def read_barcodes_from_file():
    barcode_url_map = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            for line in file:
                barcode, url = line.strip().split('|')
                barcode_url_map[barcode] = url
    return barcode_url_map

def update_barcodes_file(barcode, url):
    with open(CONFIG_FILE, 'a') as file:
        file.write(f"{barcode}|{url}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-url', methods=['POST'])
def get_url():
    barcode = request.json.get('barcode')
    barcode_url_map = read_barcodes_from_file()
    url = barcode_url_map.get(barcode, None)
    return jsonify({'url': url})

@app.route('/add-url', methods=['POST'])
def add_url():
    barcode = request.json.get('barcode')
    url = request.json.get('url')
    update_barcodes_file(barcode, url)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
