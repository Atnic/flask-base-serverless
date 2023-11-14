from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello World!'


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
