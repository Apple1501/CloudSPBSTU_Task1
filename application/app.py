from crypt import methods
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>\n"

@app.route("/number", methods=['PUT'] )
def number():
    return f"<p>result is {request.form['number']}!</p>\n"

@app.route("/command", methods=['POST'])
def command():
    return f"<p>Your Command - {request.form['command'].upper()}</p>\n"

~app.run(host='0.0.0.0', port=5000)