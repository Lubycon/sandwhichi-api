from rest_framework import serializers
from location.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'address_0', 'address_0_code',
            'address_1', 'address_1_code',
            'address_2', 'address_2_code',
        )