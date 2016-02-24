import ipdb
from flask import Flask
from flask import request
import requests
from HDFSService import webclient
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
    webclient.sendrequest(path=path, params=payload)

@app.route("/mkdir/<path>", methods=['PUT'])
def mkdir(path):
    payload = {'op': 'MKDIRS'}
    webclient.sendrequest(path=path, params=payload)


@app.route('/putintofs', methods=['POST'])
def putfile():
    local_path = request.args.get("local", "")
    dest_path = request.args.get("dest", "")
    payload = {"op": "CREATE"}
    response = webclient.sendrequest(path=dest_path, params=payload)
    datanode =response.headers["Location"]
    file = open(local_path).read()
    response = requests.put(datanode, file=file)
    return response.text

@app.route('/getfromfs/<path>', methods=['GET'])
def getfile(path):
    payload = {"op": "OPEN"}
    response = webclient.sendrequest(path=path, params=payload)
    return 'ok'

@app.route('/mov/from/<path1>/<path2>', methods=['GET'])
def movefile(path1, path2):
    print path1, path2
    return 'ok'

if __name__ == '__main__':
    app.run()