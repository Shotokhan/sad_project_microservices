from flask import Flask
import json


app = Flask(__name__)

config = {}
config_path = "./volume/config.json"
with open(config_path, 'r') as f:
    config = json.load(f)


@app.route('/', methods=['GET'])
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=config['debug'], host="0.0.0.0", port=config['port'])
