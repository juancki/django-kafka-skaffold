# Create your models here.
from django.db import models
from logpipe import Producer
from rest_framework import serializers
import uuid

class Person(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)


# Register admin
from django.contrib import admin

admin.site.register(Person)


# TODO: Change to hyperlinked
class PersonSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = 'person'
    VERSION = 1
    KEY_FIELD = 'uuid'
    PersonProducer: Producer = None

    class Meta:
        model = Person
        fields = ['uuid', 'first_name', 'last_name']

    def create(self, validated_data):
        '''
        Example of message in kafka...
        {
          "topic": "people",
          "partition": 0,
          "offset": 14,
          "tstype": "create",
          "ts": 1671929245526,
          "broker": 0,
          "key": "ddbf482b-62ab-4e80-83df-d60e43a1a19c",
          "payload": "json:{\"type\":\"person\",\"version\":1,\"message\":{\"uuid\":\"ddbf482b-62ab-4e80-83df-d60e43a1a19c\",\"first_name\":\"Joe-s33\",\"last_name\":\"Schmoe\"}}"
        }
        '''
        self.assertProducer()
        instance = Person.objects.create(**validated_data)
        self.PersonProducer.send(instance)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # After testing a bit I get that:
        # - instance is previous
        # - validated_data is incoming data
        self.assertProducer()
        self.PersonProducer.send(validated_data)
        return super().update(instance, validated_data)

    @classmethod
    def lookup_instance(cls, uuid, **kwargs):
        try:
            return Person.objects.get(uuid=uuid)
        except models.Person.DoesNotExist:
            pass

    def assertProducer(self):
        if self.PersonProducer is None:
            self.PersonProducer = Producer('people', PersonSerializer)
