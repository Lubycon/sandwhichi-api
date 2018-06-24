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

class LocationFisrtSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address_0')
    code = serializers.CharField(source='address_0_code')
    class Meta:
        model = Location
        fields = ('id', 'address', 'code')


class LocationSecondSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address_1')
    code = serializers.CharField(source='address_1_code')
    class Meta:
        model = Location
        fields = ('id', 'address', 'code')


class LocationThirdSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address_2')
    code = serializers.CharField(source='address_2_code')
    class Meta:
        model = Location
        fields = ('id', 'address', 'code', )