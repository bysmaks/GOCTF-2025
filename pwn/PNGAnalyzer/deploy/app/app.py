import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from uuid import uuid4, UUID
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/images'
app.config['ALLOWED_EXTENSIONS'] = {'png'}
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024  # 64KB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'}), 200

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', error='No file selected')
        
        file = request.files['file']
        
        # If user does not select file, browser submits empty part
        if file.filename == '':
            return render_template('upload.html', error='No file selected')
        
        if not allowed_file(file.filename):
            return render_template('upload.html', error='Only PNG files are allowed')
        
        if file and allowed_file(file.filename):
            # Read first 24 bytes to check PNG header
            header = file.stream.read(24)
            if not header.startswith(b'\211PNG\r\n\032\n'):
                return render_template('upload.html', error='Invalid PNG file')
            
            # Reset stream position after reading header
            file.stream.seek(0)
            
            # Save the file
            image_id = str(uuid4())
            filename = secure_filename(f"{image_id}.png")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return redirect(url_for('process_image', image_id=image_id))
    
    return render_template('upload.html')

@app.route('/process/<image_id>')
def process_image(image_id):
    try:
        UUID(image_id)
    except ValueError:
        return render_template('error.html', message='Invalid image ID'), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{image_id}.png")
    if not os.path.exists(file_path):
        return render_template('error.html', message='Image not found'), 404

    reverse_process = subprocess.run(
        ['/converter', file_path], 
        capture_output=True, 
        text=True,
    )

    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error deleting file: {e}")

    if reverse_process.returncode != 0:
        return render_template('error.html', message='Error processing image'), 500
    
    return render_template('result.html', result=reverse_process.stdout)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message='Internal server error'), 500
