import os
import hashlib
import shutil
from flask import request, Response, send_from_directory, jsonify, abort
from config import *


def sha1(stream):
    """
    The function returns the md5 hash,
    based on the parameters of the uploaded file.
    """
    hash_sha1 = hashlib.sha1()
    for chunk in iter(lambda: stream.read(4096), b""):
        hash_sha1.update(chunk)
    stream.seek(0)
    return hash_sha1.hexdigest()


def get_size(stream):
    """
    Function determines the size of the uploaded file.
    """
    stream.seek(0, 2)
    size = stream.tell()
    stream.seek(0)
    return size


def make_folder_for_file(file_hash):
    """
    Function determines the folder in which the downloaded file will be placed.
    """
    path = os.path.join(app.config['UPLOAD_FOLDER'],
                        file_hash[0], file_hash[1])
    if not os.path.exists(path):
        os.makedirs(os.path.join(
            app.config['UPLOAD_FOLDER'], file_hash[0], file_hash[1]))
    return path


def get_token(*args):
    token = ':'.join(str(arg) for arg in args)
    return hashlib.md5(token).hexdigest()


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    """
    The function receives a file from client, verifies the token.
    If token is successful - download a file
    and return a response with confirm token.
    """
    if request.method == 'POST':
        file = request.files['file']
        token = request.form['token']
        file_size = get_size(file.stream)
        if file and token:
            if hash_algo == 'sha1':
                file_hash = sha1(file.stream)
            file_name = file.filename.encode('utf8')
            client_ip = request.remote_addr
            if token != get_token(file_name, file_size, client_ip,
                                  args.secret):
                abort(404)
            make_folder_for_file(file_hash)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_hash[
                      0], file_hash[1], file_hash))
            confirm_token = get_token(file_name, file_size, client_ip,
                                      args.secret, file_hash)
            response = jsonify({
                "file_name": file_name,
                "file_size": file_size,
                "file_hash": file_hash,
                "confirm_token": confirm_token,
            })
            return response
        return abort(404)
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type="hidden" name="token"
        value="ca7938276d84240587df58f99f42310d">
        <input type=submit value=Upload>
        </form>
        '''


@app.route('/file/<file_hash>')
def get_file(file_hash):
    """
    Return requested file to client
    """
    folder = os.path.join(
        app.config['UPLOAD_FOLDER'], file_hash[0], file_hash[1])
    if folder:
        return send_from_directory(folder,
            file_hash), {'Content-Type': 'audio/mpeg; charset=utf-8'}
    else:
        abort(404)


@app.route('/file/<file_hash>', methods=['DELETE'])
def delete_file(file_hash):
    """
    Delete requested file
    """
    file = os.path.join(app.config['UPLOAD_FOLDER'], file_hash[
                        0], file_hash[1], file_hash)
    if file:
        os.remove(file)
        return 'remove %s' % file_hash
    else:
        abort(404)


@app.route('/status', methods=['GET'])
def get_status():
    """
    Function displays the remaining free space on the disk
    """
    disc = os.statvfs(BASE_DIR)
    free_space = disc.f_bsize * disc.f_bavail
    return jsonify({'free_space': free_space})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=args.port, threaded=True)
