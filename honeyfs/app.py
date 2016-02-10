
from flask import Flask
from HDFSClient import sendrequest
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello HoneyFS!'

@app.route("/health")
def health():
    return 'ok'

@app.route("/ls/<path>", methods=['GET'])
def ls(path):
    payload = {'op': 'LISTSTATUS'}
    sendrequest(path=path, params=payload)

@app.route("/mkdir/<path>", methods=['PUT'])
def ls(path):
    payload = {'op': 'MKDIRS'}
    sendrequest(path=path, params=payload)


@app.route('/putintofs/<path>', methods=['POST'])
def putfile():
    return 'ok'

@app.route('/getfromfs/<path>', methods=['GET'])
def getfile(path):
    print path
    return 'ok'

@app.route('/mov/from/<path1>/<path2>', methods=['GET'])
def movefile(path1, path2):
    print path1, path2
    return 'ok'

if __name__ == '__main__':
    app.run()