from rest_framework.response import Response
from rest_framework import status, viewsets
from location.models import Location
from location.serializers import LocationFisrtSerializer, LocationSecondSerializer, LocationThirdSerializer

class LocationViewSet(viewsets.ModelViewSet):
    """
    주소 리스트 API
    """
    def first_list(self, request, *args, **kwargs):
        locations = Location.objects.filter(address_1_code__isnull=True, address_2_code__isnull=True, )
        serializer = LocationFisrtSerializer(locations, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def second_list(self, request, *args, **kwargs):
        locations = Location.objects.filter(
            address_0_code=kwargs.get('address_0_code', ''),
            address_1_code__isnull=False,
            address_2_code__isnull=True,
        )
        serializer = LocationSecondSerializer(locations, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def third_list(self, request, *args, **kwargs):
        locations = Location.objects.filter(
            address_0_code=kwargs.get('address_0_code', ''),
            address_1_code=kwargs.get('address_1_code', ''),
            address_2_code__isnull=False,
        )
        serializer = LocationThirdSerializer(locations, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)