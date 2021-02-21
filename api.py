from bottle import post, get, run, template, request, response, Response, HTTPError, HTTPResponse
from bank.manager import Manager
from bank.event import Event
from helpers import *

manager = Manager()

@post('/reset')
def reset():
    manager.reset()

    return 'OK'

@get('/balance')
def balance():
    if 'account_id' in request.query:
        account_id = request.query['account_id']
        success, balance = manager.get_account_balance(account_id)
        if success:
            return str(balance)

    return text_response(404, '0')

@post('/event')
def event():
    event = Event(request.json, manager)
    success, result = event.execute()
    if success:
        return json_response(201, result)

    return text_response(404, '0')


run(host='localhost', port=3000)
