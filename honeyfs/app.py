
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello HoneyFS!'

@app.route("/health")
def health():
    return 'ok'

@app.route('/putintofs/<path>', methods=['POST'])
def putfile():
    return 'ok'

if __name__ == '__main__':
    app.run()
