# Python utilities
from binascii import a2b_base64
from os import system
import os.path

# server stuff (pip install bottle)
from bottle import BaseRequest, route, run, view, static_file, request


# allow the big image uploads
BaseRequest.MEMFILE_MAX = 1024 * 1024

# go from the browser's base64 image to an image file
def saveImage(url, fname):
    binary_data = a2b_base64(url[url.find('base64') + 7:])
    fd = open('input/' + fname + '_alpha', 'wb')
    fd.write(binary_data)
    fd.close()
    # remove alpha channel from <canvas> images
    system('convert -alpha off input/' + fname + '_alpha input/' + fname)

# homepage
@route('/')
@view('index_template')
def index():
    return {}

# faces experiment
@route('/faces')
@view('faces_template')
def faces():
    return {}

@route('/monster')
@view('monster_template')
def monster():
    return {}

# receive images and start up TensorFlow
@route('/spawn', method='POST')
@view('started_template')
def spawn():
    if (request.forms.get('experiment') == 'faces'):
        original = request.forms.get('original')
        saveImage(original, 'original.jpg')
        system('rm output/a*.png')
        system('../image-analogies/scripts/make_image_analogy.py output/sugarskull-A.jpg output/sugarskull-Ap.jpg input/original.jpg output/a --patch-size=3 &')
    elif (request.forms.get('experiment') == 'monster'):
        original = request.forms.get('original')
        saveImage(original, 'original.jpg')
        system('rm output/a*.png')
        system('../image-analogies/scripts/make_image_analogy.py output/monster-A.jpg output/monster-Ap.jpg input/original.jpg output/a --patch-size=3 &')
    else:
        original = request.forms.get('original')
        mask = request.forms.get('mask')
        newMask = request.forms.get('new-mask')
        saveImage(original, 'original.jpg')
        saveImage(mask, 'mask.jpg')
        saveImage(newMask, 'new-mask.jpg')
        system('rm output/a*.png')
        system('../image-analogies/scripts/make_image_analogy.py input/mask.jpg input/original.jpg input/new-mask.jpg output/a --patch-size=3 &')
    return {}

@route('/spawn', method='GET')
@view('started_template')
def spawn_land():
    return {}

# check results
@route('/results')
@view('results_template')
def results():
    return {}

# output images (show blank if not existing yet)
@route('/output/<path>')
def output(path):
    path = path.replace('..', '')
    if (os.path.isfile('./output/' + path)):
        return static_file(path, './output')
    else:
        return static_file('missing.png', './output')

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
