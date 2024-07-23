from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os

app = Flask(__name__)

EFS_PATH = "/mnt/efs/fs1"  # Adjust this path based on your EFS mount point

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_dir = os.path.join(EFS_PATH, username)

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        return redirect(url_for('user_files', username=username))

    return '''
        <form method="post">
            <input type="text" name="username" required>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/<username>')
def user_files(username):
    user_dir = os.path.join(EFS_PATH, username)
    if not os.path.exists(user_dir):
        return "User directory not found", 404

    files = os.listdir(user_dir)
    files.sort()
    return render_template('files.html', username=username, files=files)

@app.route('/<username>/upload', methods=['POST'])
def upload_file(username):
    user_dir = os.path.join(EFS_PATH, username)
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file.save(os.path.join(user_dir, file.filename))
        return redirect(url_for('user_files', username=username))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
