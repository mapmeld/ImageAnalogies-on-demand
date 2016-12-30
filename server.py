# Python utilities
from binascii import a2b_base64
from os import system
import os.path, json, subprocess

# server stuff (pip install bottle)
from bottle import BaseRequest, route, run, view, static_file, request


# allow the big image uploads
BaseRequest.MEMFILE_MAX = 1024 * 1024

# monitor if anyone has given the server a task yet
given_task = False
started_task = False
finished_task = False

# go from the browser's base64 image to an image file
def saveImage(url, fname):
    binary_data = a2b_base64(url[url.find('base64') + 7:])
    fd = open('input/' + fname + '_alpha', 'wb')
    fd.write(binary_data)
    fd.close()
    # remove alpha channel from <canvas> images
    system('convert -alpha off input/' + fname + '_alpha input/' + fname)

# based on http://stackoverflow.com/questions/7647167/check-if-a-process-is-running-in-python-in-linux-unix
def findProcess(process_name):
    ps = subprocess.Popen("ps aux | grep " + process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return output.split('\n')

# homepage
@route('/')
@view('index_template')
def index():
    return {}

# status.json
@route('/status')
def status():
    # determine at check-time if task has finished
    if started_task and not finished_task:
       matching_processes = findProcess('make_image')
       if len(matching_processes) == 3:
           finished_task = True

    stat = {
      "serving": True, # always true while server is on
      "started_task": started_task,
      "finished_task": finished_task
    }
    return json.dumps(stat)

# receive images and start up TensorFlow
@route('/spawn', method='POST')
def spawn():
    # update tasking status
    given_task = True
    finished_task = False

    system('rm output/a*.png')
    original = request.forms.get('original')
    mask = request.forms.get('mask')
    newMask = request.forms.get('new-mask')
    saveImage(original, 'original.jpg')
    saveImage(mask, 'mask.jpg')
    saveImage(newMask, 'new-mask.jpg')

    system('python task.py &')
    started_task = True
    return json.dumps({ spawned: True })

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

# static files
@route('/js/<path>')
@route('/css/<path>')
def staticstuff(path):
    return static_file(path.replace('..', ''), './static')

run(host='localhost', port=8080)
