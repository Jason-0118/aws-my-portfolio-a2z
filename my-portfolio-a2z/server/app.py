from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)
app.secret_key = b'\x9f\x82\x8d\xf3\xe8\xbb\xf0\xa3\xcb\x1c\x87\xf8\x8b\xe3\x9e\xae\x9a\xf6\xb2\x88\x97\xc6\x84\x85'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Configure AWS S3
s3 = boto3.client('s3')
bucket_name = 's3-efs-v1'
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

def list_s3_objects(username):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{username}/')
        objects = response.get('Contents', [])
        sorted_objects = sorted(objects, key=lambda obj: obj['LastModified'], reverse=True)
        return [obj['Key'].split(f'{username}/')[1] for obj in sorted_objects if obj['Key'] != f'{username}/']
    except ClientError as e:
        logger.error(f'Error listing S3 objects: {e}')
        return []


@app.route('/<username>')
def user_files(username):
    user_dir = os.path.join(EFS_PATH, username)
    if not os.path.exists(user_dir):
        return "User directory not found", 404

    files = os.listdir(user_dir)
    files.sort()
    s3_files = list_s3_objects(username)
    return render_template('files.html', username=username, files=files, s3_files=s3_files)

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

@app.route('/<username>/delete/<filename>', methods=['POST'])
def delete_file(username, filename):
    user_dir = os.path.join(EFS_PATH, username)
    file_path = os.path.join(user_dir, filename)

    if os.path.exists(file_path):
        # First, move the file to S3 bucket
        s3_path = f'{username}/{filename}'
        try:
            s3.upload_file(file_path, bucket_name, s3_path)
            os.remove(file_path)
            flash(f'File {filename} deleted and moved to S3', 'success')
        except FileNotFoundError:
            flash('File not found', 'danger')
        except NoCredentialsError:
            flash('AWS credentials not available', 'danger')
        except ClientError as e:
            flash(f'Error uploading file to S3: {e}', 'danger')
    else:
        flash('File does not exist', 'danger')
    
    return redirect(url_for('user_files', username=username))


@app.route('/<username>/restore/<filename>', methods=['POST'])
def restore_file(username, filename):
    user_dir = os.path.join(EFS_PATH, username)
    file_path = os.path.join(user_dir, filename)
    s3_path = f'{username}/{filename}'

    try:
        s3.download_file(bucket_name, s3_path, file_path)
        flash(f'File {filename} restored from S3 to EFS', 'success')
    except ClientError as e:
        flash(f'Error downloading file from S3: {e}', 'danger')

    return redirect(url_for('user_files', username=username))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

