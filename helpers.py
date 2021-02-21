import json
from bottle import HTTPResponse

def json_response(status, data):
    headers = {'Content-type': 'application/json'}

    return HTTPResponse(status=status, body=json.dumps(data), headers=headers)

def text_response(status, text):
    return HTTPResponse(status=status, body=text)