# Weekly.TF

Project to spin up TensorFlow instances for custom user runs.

## Setup

### Configure TensorFlow machine

Install TensorFlow and <a href='https://github.com/awentzonline/image-analogies'>Image Analogies</a> (the current test project).  On Amazon EC2, you can start with Amazon's Deep Learning AMI on a GPU server.

Make sure to download the vgg16_weights.h5 file.

Debugging: test that Amazon AMI is truly using GPU
http://stackoverflow.com/questions/38009682/how-to-tell-if-tensorflow-is-using-gpu-acceleration-from-inside-python-shell

### Start server

Start the server as a background process:

```
nohup python server.py &
```

Go to the index page ( http://localhost:8080/ ), click the 'Test Case' button, and then Run.

On AWS: use a g2.2xlarge instance with port 80 open, and ensure that httpd is running, and ProxyPass / http://localhost:8080/

## License

Open source, MIT license
