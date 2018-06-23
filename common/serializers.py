from rest_framework import serializers
from common.models import (
    ContactType, Contact, MediaType, Media, Ability, Keyword
)

class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ('id', 'name')


class ContactSerializer(serializers.ModelSerializer):
    type = ContactTypeSerializer()
    class Meta:
        model = Contact
        fields = ('type', 'information')


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('type', 'information')


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ('id', 'name')


class MediaSerializer(serializers.ModelSerializer):
    type = MediaTypeSerializer()
    class Meta:
        model = Media
        fields = ('type', 'url')


class MediaCreateSerializer(serializers.ModelSerializer):
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