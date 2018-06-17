from rest_framework import serializers
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from project.models import (
    Project, Schedule, DescriptionQuestion,
    ProjectDescription, ScheduleRecurringType
)
from common.models import (
    Ability, Keyword
)
from common.serializers import (
    ContactSerializer, MediaSerializer
)


class ScheduleRecurringTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleRecurringType
        fields = ('id', 'name', )


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule


class DescriptionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionQuestion
        fields = ('id', 'question')


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDescription
        fields = ('id', 'question', 'answer')


class ProjectCreateSerializer(serializers.ModelSerializer):
    description = ProjectDescriptionSerializer(many=True, )
    media = MediaSerializer(many=True, )
    contacts = ContactSerializer(many=True, )
    abilities = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'profile_image',
            'started_at',
            'ends_at',
            'media',
            'contacts',
            'abilities',
            'keywords'
        )
    
    def create(self, validated_data):
        # new_project = Project.objects.create_new_project(**validated_data)
        abilities_data = validated_data.pop('abilities')
        keywords_data = validated_data.pop('keywords')

        project = Project(**validated_data)

        for ability_string in abilities_data:
            ability = Ability.objects.get_or_create(name=ability_string)
            ability.count += 1
            ability.save()
            project.abilities.add(ability)
        
        for keyword_string in keywords_data:
            keyword = Keyword.objects.get_or_create(name=keyword_string)
            keyword.count += 1
            keyword.save()
            project.keywords.add(keyword)
        
        project.save()
        return project
        

            

    