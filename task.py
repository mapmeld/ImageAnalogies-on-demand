# run the task async
# then upload results

from os import system
import s3upload

try:
    # clear old images
    system('rm output/a*.png')
    # create_bucket(task_id)
except:
    s = 1

try:
    system('../image-analogies/scripts/make_image_analogy.py input/mask.jpg input/original.jpg input/new-mask.jpg output/a --patch-size=3')
except:
    system('wget https://superhero.tf/error?err=?')
finally:
    # force finished_task status update by checking the status
    system('wget http://localhost:8080/status')
    
    # upload images to S3