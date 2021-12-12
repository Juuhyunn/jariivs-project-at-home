from datetime import datetime

from django.db import models
from django.db.models import IntegerField, CharField
from django_mysql.models import ListTextField


# Create your models here.
from rest_framework import serializers
from routine.models import Routine as routine


class RoutineSerializer(serializers.Serializer):
    id = serializers.CharField()
    create_date = serializers.CharField()
    log_repeat = serializers.CharField()
    priority = serializers.CharField()
    grade = serializers.CharField()
    contents = serializers.CharField()
    location = serializers.CharField()
    cron = serializers.CharField()
    days = serializers.CharField()
    hours = serializers.CharField()
    log_id = serializers.CharField()
    user_id = serializers.CharField()

    class Meta:
        model = routine
        fileds = '__all__'

    def create(self, validated_data):
        return routine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        routine.objects.filter(pk=instance.id).update(**validated_data)