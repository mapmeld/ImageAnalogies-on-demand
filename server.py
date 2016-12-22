import os
from bottle import route, run, view, static_file

# homepage
@route('/')
@view('index_template')
def index():
    return {}

# test image
@route('/test-case/<path>')
def test_cases(path):
    return static_file(path.replace('..', ''), './test-case')

# static files
@route('/js/<path>')
@route('/css/<path>')
def staticstuff(path):
    return static_file(path.replace('..', ''), './static')

run(host='localhost', port=8080)
