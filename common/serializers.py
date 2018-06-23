from rest_framework import serializers
from common.models import (
    Contact, Media, Ability, Keyword
)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('type', 'information')


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('type', 'url')


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ('id', 'name', 'count')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'name', 'count')