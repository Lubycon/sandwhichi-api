from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import (MultipleObjectsReturned, ObjectDoesNotExist, )
from project.models import (
    Project, Schedule, DescriptionQuestion,
    ProjectDescription, ScheduleRecurringType,
)
from common.models import (
    Ability, Keyword, Contact, Media,
)
from common.serializers import (
    ContactCreateSerializer, MediaCreateSerializer,
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
        fields = ('project', 'question', 'answer')

    def create(self, validated_data):
        print('validated -> ', validated_data)
        new_project_description = ProjectDescription.objects.create(**validated_data)
        new_project_description.save()
        return new_project_description


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
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


class ProjectCreateSerializer(serializers.ModelSerializer):
    descriptions = ProjectDescriptionSerializer(many=True, )
    media = MediaCreateSerializer(many=True, )
    contacts = ContactCreateSerializer(many=True, )
    abilities = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Project
        fields = (
            'title',
            'descriptions',
            'profile_image',
            'started_at',
            'ends_at',
            'media',
            'contacts',
            'abilities',
            'keywords'
        )
    
    @transaction.atomic
    def create(self, validated_data):
        descriptions_data = validated_data.pop('descriptions')
        abilities_data = validated_data.pop('abilities')
        keywords_data = validated_data.pop('keywords')
        media_data = validated_data.pop('media')
        contacts_data = validated_data.pop('contacts')

        project = Project.objects.create(**validated_data)
        project.save()

        for description_data in descriptions_data:
            description_data['project'] = project.id
            description_data['question'] = description_data['question'].id
            description = ProjectDescriptionSerializer(data=description_data)
            if description.is_valid():
                description.save()
            else:
                raise ValueError(description.errors)

        for media_data_object in media_data:
            media = Media(type=media_data_object['type'], url=media_data_object['url'])
            media.save()
            project.media.add(media)

        for contact_data in contacts_data:
            contact = Contact(type=contact_data['type'], information=contact_data['information'])
            contact.save()
            project.contacts.add(contact)

        for ability_string in abilities_data:
            ability, created = Ability.objects.get_or_create(name=ability_string)

            if not created:
                new_count = ability.count + 1
                ability.count = new_count
            ability.save()
            project.abilities.add(ability)
        
        for keyword_string in keywords_data:
            keyword, created = Keyword.objects.get_or_create(name=keyword_string)

            if not created:
                new_count = keyword.count + 1
                keyword.count = new_count
            keyword.save()
            project.keywords.add(keyword)
        
        project.save()
        return project
        

            

    