from flask import Flask, request, jsonify
from datetime import datetime
import hashlib

app = Flask(__name__)
app.token_list = []


def remove_token(token):
    new_token_list = []
    for tk in app.token_list:
        if tk != token:
            new_token_list.append(tk)
    app.token_list = new_token_list


@app.route('/api/v1/token/generate')
def generate():
    if request.method == 'GET':
        hash_object = hashlib.sha256(str(datetime.now()).encode('utf-8'))
        token = hash_object.hexdigest()
        app.token_list.append(token)
        return jsonify({"code": 200, "message": "success", "data": {"token": token}})
    else:
        return jsonify({"code": 400, "message": "bad request", "data": {}})


@app.route('/api/v1/token/validate', methods=['POST'])
def validate():
    if request.method == 'POST':
        token = request.form.get('token')
        if token in app.token_list:
            remove_token(token)
            return jsonify({"code": 200, "message": "success", "status": "approved"})
        else:
            return jsonify({"code": 200, "message": "success", "status": "rejected"})
    else:
        return jsonify({"code": 400, "message": "bad request", "status": "rejected"})


if __name__ == '__main__':
    app.run()
