# Python utilities
from binascii import a2b_base64

# server stuff (pip install bottle)
from bottle import BaseRequest, route, run, view, static_file, request


# allow the big image uploads
BaseRequest.MEMFILE_MAX = 1024 * 1024

def saveImage(url, fname):
    binary_data = a2b_base64(url[url.find('base64') + 7:])
    fd = open(fname, 'wb')
    fd.write(binary_data)
    fd.close()

# homepage
@route('/')
@view('index_template')
def index():
    return {}

# receive images and start up TensorFlow
@route('/spawn', method='POST')
@view('started_template')
def spawn():
    original = request.forms.get('original')
    mask = request.forms.get('mask')
    newMask = request.forms.get('new-mask')
    saveImage(original, 'original.jpg')
    saveImage(mask, 'mask.jpg')
    saveImage(newMask, 'new-mask.jpg')
    return {}

# check results
@route('/results')
@view('results_template')
def results():
    return {}

# test image (static)
@route('/test-case/<path>')
def test_cases(path):
    return static_file(path.replace('..', ''), './test-case')

# static files
@route('/js/<path>')
@route('/css/<path>')
def staticstuff(path):
    return static_file(path.replace('..', ''), './static')

run(host='localhost', port=8080)
