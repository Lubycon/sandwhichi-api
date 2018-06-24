from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from location.models import Location
from location.serializers import LocationSerializer

class LocationViewSet(APIView):
    """
    주소 리스트 API
    """
    def get(self, request, format='json'):
        locations = Location.objects.all()
        print(locations)
        serializer = LocationSerializer(locations, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)
