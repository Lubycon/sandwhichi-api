from PIL import Image
import boto3
from django.conf import settings
import uuid
import io
import json

s3 = boto3.resource('s3',
                    region_name=settings.RAW_IMAGE_BUCKET_REGION_NAME,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
raw_bucket_name = settings.RAW_IMAGE_BUCKET_NAME
service_bucket_name = 'sandwhichi-dev'


def responsive_image(key, json_sizes, extension):
    sizes = json.loads(json_sizes)
    raw_bucket = s3.Bucket(raw_bucket_name)
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
    raw_bucket.download_file(key, download_path)
    for size in sizes:
        resize_image(download_path, key, size, extension)
    return True


def resize_image(image_path, key, size, extension):
    buffer = io.BytesIO()
    s3_object = s3.Object(service_bucket_name, "{}{}".format(key, size))

    image = Image.open(image_path)
    wpercent = (size / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image.resize((size, hsize))
    image.save(buffer, extension)
    buffer.seek(0)  # rewind pointer back to start
    response = s3_object.put(
        Body=buffer,
        ContentType='image/{}'.format(extension),
    )
