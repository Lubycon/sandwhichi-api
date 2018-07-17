from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.throttling import UserRateThrottle
from base.exceptions import BadFileRequest, InternalServerError

import io
import boto3
import uuid
import datetime
from django.conf import settings

from .tasks import responsive_image

from PIL import Image
import json


class ImageViewSet(APIView):
    # DRF settings
    throttle_classes = (UserRateThrottle,)
    parser_classes = (MultiPartParser,)

    # Image ex white list
    allowed_image_format = ['JPEG', 'PNG']
    max_image_size = 3145728  # byte
    image_size = (100, 360, 720, 1920)

    def post(self, request):
        if 'image' not in request.FILES:
            raise BadFileRequest('파일이 없습니다.')

        buffer = io.BytesIO()
        request_image = request.FILES['image']
        request_image_size = request_image.size

        if request_image_size > self.max_image_size:
            raise BadFileRequest('파일이 너무 큽니다. 파일은 %s byte 이하여야 합니다.' % (self.max_image_size))

        s3 = boto3.resource('s3',
                            region_name=settings.SANDWHICHI_RAW_IMAGE_BUCKET_REGION_NAME,
                            aws_access_key_id=settings.SANDWHICHI_RAW_IMAGE_AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.SANDWHICHI_RAW_IMAGE_AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.SANDWHICHI_RAW_IMAGE_BUCKET_NAME

        try:
            image_file = Image.open(request_image)
            image_format = image_file.format
        except Exception as error:
            raise BadFileRequest(str(error))

        if image_format not in self.allowed_image_format:
            raise BadFileRequest('지원하지 않는 파일 포맷입니다;')

        image_content_type = "image/%s" % (image_format.lower())

        try:
            image_file.save(buffer, image_format)
            buffer.seek(0)  # rewind pointer back to start
        except Exception as error:
            raise InternalServerError('이미지를 처리하던 중 알 수 없는 에러가 발생하였습니다. 문제가 계속 되면 고객센터로 문의해주세요.')

        if image_file:
            # Tag this file_name with an expiry time
            file_name = "%s-%s" % (uuid.uuid4(), datetime.datetime.now().strftime("%Y%m%d%H"))
            image_url = "%s%s" % (settings.SANDWHICHI_RAW_IMAGE_BUCKET_BASE_URL, file_name)
            s3_object = s3.Object(bucket_name, file_name)

            # try:
            response = s3_object.put(
                Body=buffer,
                ContentType=image_content_type,
            )
            json_size = json.dumps(self.image_size)
            responsive_image(file_name, json_size, image_format.lower())
            # except Exception as error:
            #     # TODO Add error tracker...
            #     return Response({
            #         "status": {
            #             "code": "9999",
            #             "msg": str(error),
            #             "devMsg": "",
            #         },
            #         "result": {}
            #     }, status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({ 'url': image_url, }, status.HTTP_200_OK)
