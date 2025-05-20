import os
from flask import Flask, jsonify, request
from uuid import uuid4, UUID
import subprocess
import base64
app = Flask(__name__)
@app.route('/')
def ping():
    return jsonify({'status': 'ok'}), 200


@app.route("/")


@app.route('/reverse', methods=['POST'])
def reverse_image():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'status': 'error', 'message': 'No image provided'}), 400
    
    data = data['image']
    data = base64.b64decode(data)
    if not data:
        return jsonify({'status': 'error', 'message': 'No image provided'}), 400
    # if len(data) < 1024:
    #     return jsonify({'status': 'error', 'message': 'Image too small'}), 400    
    if len(data) > 1024 * 64:
        return jsonify({'status': 'error', 'message': 'Image too large'}), 413
    
    header = data[:24]
    if not header.startswith(b'\211PNG\r\n\032\n'):
        return jsonify({'status': 'error', 'message': 'Invalid PNG image'}), 400
    
    image_id = str(uuid4())
    if not os.path.exists('/tmp/images'):
        os.makedirs('/tmp/images')

    with open(f'/tmp/images/{image_id}.png', 'wb') as f:
        f.write(data)

    return jsonify({'status': 'ok', 'uuid': image_id}), 200

@app.route('/reverse/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        UUID(image_id)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid image id'}), 400

    reverse_process = subprocess.run(
        ['/converter', f'/tmp/images/{image_id}.png'], capture_output=True, text=True,
    )

    try:
        os.remove(f'/tmp/images/{image_id}.png')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    if reverse_process.returncode != 0:
        return jsonify({'status': 'error', 'message': f'Error processing image, {reverse_process.stdout}'}), 500
    
    return jsonify({'status': 'ok', 'result': reverse_process.stdout}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500