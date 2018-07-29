from rest_framework import serializers
from django.db import transaction
from project.models import (
    Project, DescriptionQuestion,
    ProjectDescription, ScheduleRecurringType, Schedule,
    ProjectMember
)
from common.models import (
    Ability, Keyword, Contact, Media,
)
from location.models import Location
from common.serializers import (
    ContactSerializer, ContactSaveSerializer,
    MediaSerializer, MediaSaveSerializer,
    AbilitySerializer, KeywordSerializer
)
from user.serializers import UserSimpleSerializer
from location.serializers import LocationSerializer


class ScheduleRecurringTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleRecurringType
        fields = ('id', 'name', )


class ScheduleSaveSerializer(serializers.ModelSerializer):
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
    content = serializers.CharField(source='question')
    class Meta:
        model = DescriptionQuestion
        fields = ('id', 'content')


class ProjectDescriptionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDescription
        fields = ('question', 'answer')


class ProjectDescriptionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = ProjectDescription
        fields = ('id', 'question', 'answer')
    
    def get_question(self, obj):
        question = DescriptionQuestion.objects.get(pk=obj.question.id)
        return DescriptionQuestionSerializer(question).data


class ProjectMemberSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    user = UserSimpleSerializer()

    class Meta:
        model = ProjectMember
        fields = ('role', 'user', )


class ProjectSerializer(serializers.ModelSerializer):
    descriptions = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
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
            'members',
        )
    
    def get_descriptions(self, obj):
        descriptions = ProjectDescription.objects.filter(project=obj.id)
        return ProjectDescriptionSerializer(descriptions, many=True).data

    def get_members(self, obj):
        members = ProjectMember.objects.filter(project=obj.id, is_active=True, )
        return ProjectMemberSerializer(members, many=True).data


class ProjectSaveSerializer(serializers.ModelSerializer):
    descriptions = ProjectDescriptionSaveSerializer(many=True, )
    media = MediaSaveSerializer(many=True, )
    contacts = ContactSaveSerializer(many=True, )
    schedule = ScheduleSaveSerializer()
    abilities = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())
    location_code = serializers.CharField(source='location')

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
            'location_code',
        )

    def __init__(self, http_request=None, *args, **kwargs):
        self.http_request = http_request

        # Instantiate the superclass normally
        super(ProjectSaveSerializer, self).__init__(*args, **kwargs)

    @transaction.atomic
    def create(self, validated_data):
        descriptions_data = validated_data.pop('descriptions')
        abilities_data = validated_data.pop('abilities')
        keywords_data = validated_data.pop('keywords')
        media_data = validated_data.pop('media')
        contacts_data = validated_data.pop('contacts')
        schedule_data = validated_data.pop('schedule')

        user = self.http_request.user

        # One to One
        schedule_serializer = ScheduleSaveSerializer(data=schedule_data)
        if schedule_serializer.is_valid():
            schedule = schedule_serializer.save()
        else:
            raise ValueError(schedule_serializer.errors)

        location = Location.objects.get(address_1_code=validated_data.get('location'), address_2_code__isnull=True)

        project = Project.objects.create(
            title=validated_data['title'],
            profile_image=validated_data['profile_image'],
            started_at=validated_data['started_at'],
            ends_at=validated_data['ends_at'],
            location=location,
            schedule=schedule,
        )
        project.save()

        # Many to Many
        for description_data in descriptions_data:
            description = ProjectDescription(
                project=project,
                question=description_data.get('question'),
                answer=description_data.get('answer'),
            )
            description.save()

        for media_data_object in media_data:
            media = Media(
                type=media_data_object.get('type'),
                url=media_data_object.get('url'),
            )
            media.save()
            project.media.add(media)

        for contact_data in contacts_data:
            contact = Contact(
                type=contact_data.get('type'),
                information=contact_data.get('information'),
            )
            contact.save()
            project.contacts.add(contact)

        for ability_string in abilities_data:
            ability, created = Ability.objects.get_or_create(name=ability_string)
            new_count = ability.count + 1
            ability.count = new_count

            ability.save()
            project.abilities.add(ability)
        
        for keyword_string in keywords_data:
            keyword, created = Keyword.objects.get_or_create(name=keyword_string)
            new_count = keyword.count + 1
            keyword.count = new_count

            keyword.save()
            project.keywords.add(keyword)
        
        project.save()

        # Set project admin
        project_admin = ProjectMember(
            project=project,
            user=user,
            role='admin'
        )
        project_admin.save()

        return project
