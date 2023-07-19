from flask import Flask

app = Flask(__name__)

test = "qweqweqwe" 

@app.route("/")
def hello_world():
    return f'<p>{test}</p>'