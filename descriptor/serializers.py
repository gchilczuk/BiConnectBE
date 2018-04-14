from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email',
                  'username', 'member', 'group',
                  'newsletter', 'speech_confirm')
