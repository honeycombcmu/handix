__author__ = 'handixu'
import requests

address = 'http://localhost'
port = '50070'
def sendrequest(path, param):
    return requests.get(address+':'+port+'/webhdfs/v1' + path, param)
