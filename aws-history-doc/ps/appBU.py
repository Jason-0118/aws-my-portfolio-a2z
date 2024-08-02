from flask import Flask, request, jsonify
import os
import json
import logging

app = Flask(__name__)
UPLOAD_FOLDER = '/mnt/efs/fs1'  # Path to your mounted EFS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(filename='/var/log/flask_app/flask_app.log', level=logging.DEBUG)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part')
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify(error='No selected file'), 400
    if file:
        try:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            app.logger.info(f'File saved to {file_path}')

            # Append to notes.json
            notes_file = os.path.join(app.config['UPLOAD_FOLDER'], 'notes.json')
            if not os.path.exists(notes_file):
                with open(notes_file, 'w') as f:
                    json.dump([], f)

            with open(notes_file, 'r+') as f:
                notes = json.load(f)
                notes.append({"file": filename})
                f.seek(0)
                json.dump(notes, f, indent=4)
                f.truncate()

            return jsonify(message='File successfully uploaded and noted'), 200
        except Exception as e:
            app.logger.error(f'Error: {e}')
            return jsonify(error='Internal Server Error'), 500

if __name__ == '__main__':
