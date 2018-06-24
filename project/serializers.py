from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import (MultipleObjectsReturned, ObjectDoesNotExist, )
from project.models import (
    Project, Schedule, DescriptionQuestion,
    ProjectDescription, ScheduleRecurringType, Schedule,
)
from common.models import (
    Ability, Keyword, Contact, Media,
)
from common.serializers import (
    ContactSerializer, ContactCreateSerializer,
    MediaSerializer, MediaCreateSerializer,
    AbilitySerializer, KeywordSerializer
)
from location.serializers import LocationSerializer


class ScheduleRecurringTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleRecurringType
        fields = ('id', 'name', )


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
            'is_negotiable',
            'recurring_type',
            'start_time',
            'end_time',
        )


class ScheduleSerializer(serializers.ModelSerializer):
    recurring_type = ScheduleRecurringTypeSerializer()
    class Meta:
        model = Schedule
        fields = (
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
            'is_negotiable',
            'recurring_type',
            'start_time',
            'end_time',
        )


class DescriptionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionQuestion
        fields = ('id', 'question')


class ProjectDescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDescription
        fields = ('question', 'answer')


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = ProjectDescription
        fields = ('question', 'answer')
    
    def get_question(self, obj):
        print(obj.question)
        question = DescriptionQuestion.objects.get(pk=obj.question.id)
        return DescriptionQuestionSerializer(question).data['question']


class ProjectSerializer(serializers.ModelSerializer):
    descriptions = serializers.SerializerMethodField()
    media = MediaSerializer(many=True, )
    contacts = ContactSerializer(many=True, )
    abilities = AbilitySerializer(many=True, )
    keywords = KeywordSerializer(many=True, )
    schedule = ScheduleSerializer()
    location = LocationSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'descriptions',
            'profile_image',
            'started_at',
            'ends_at',
            'media',
            'contacts',
            'abilities',
            'keywords',
            'schedule',
            'location',
        )
    
    def get_descriptions(self, obj):
        descriptions = ProjectDescription.objects.filter(project=obj.id)
        return ProjectDescriptionSerializer(descriptions, many=True).data


class ProjectCreateSerializer(serializers.ModelSerializer):
    descriptions = ProjectDescriptionCreateSerializer(many=True, )
    media = MediaCreateSerializer(many=True, )
    contacts = ContactCreateSerializer(many=True, )
    schedule = ScheduleCreateSerializer()
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
            'keywords',
            'schedule',
            'location',
        )
    
    @transaction.atomic
    def create(self, validated_data):
        descriptions_data = validated_data.pop('descriptions')
        abilities_data = validated_data.pop('abilities')
        keywords_data = validated_data.pop('keywords')
        media_data = validated_data.pop('media')
        contacts_data = validated_data.pop('contacts')
        schedule_data = validated_data.pop('schedule')

        # One to One
        print(validated_data)
        schedule_serializer = ScheduleCreateSerializer(data=schedule_data)
        if schedule_serializer.is_valid():
            schedule = schedule_serializer.save()
        else:
            raise ValueError(schedule_serializer.errors)

        project = Project.objects.create(
            title=validated_data['title'],
            profile_image=validated_data['profile_image'],
            started_at=validated_data['started_at'],
            ends_at=validated_data['ends_at'],
            location=validated_data['location'],
            schedule=schedule
        )
        project.save()


        # Many to Many
        for description_data in descriptions_data:
            description = ProjectDescription(
                project=project,
                question=description_data['question'],
                answer=description_data['answer']
            )
            description.save()

        for media_data_object in media_data:
            media = Media(
                type=media_data_object['type'],
                url=media_data_object['url']
            )
            media.save()
            project.media.add(media)

        for contact_data in contacts_data:
            contact = Contact(
                type=contact_data['type'],
                information=contact_data['information']
            )
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
        

            

    