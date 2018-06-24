from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.models import ContactType, MediaType
from common.serializers import ContactTypeSerializer, MediaTypeSerializer

class ContactTypeViewSet(APIView):
    """
    연락처 타입 리스트 API
    """
    def get(self, request, format='json'):
        contact_types = ContactType.objects.all()
        serializer = ContactTypeSerializer(contact_types, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaTypeViewSet(APIView):
    """
    미디어 타입 리스트 API
    """
    def get(self, request, format='json'):
        media_types = MediaType.objects.all()
        serializer = MediaTypeSerializer(media_types, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)