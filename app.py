from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html', filename=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return render_template('index.html', filename=filename)
    return redirect(request.url)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_color', methods=['POST'])
def get_color():
    data = request.json
    filename = data['filename']
    x = data['x']
    y = data['y']
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with Image.open(filepath) as img:
        img = img.convert("RGB")
        r, g, b = img.getpixel((x, y))

    color_name = "Unknown Color"  # You can replace this with a function that converts RGB to a color name

    response = {
        'R': r,
        'G': g,
        'B': b,
        'color_name': color_name
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
