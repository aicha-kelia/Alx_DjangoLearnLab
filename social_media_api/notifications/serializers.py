from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    actor_id = serializers.ReadOnlyField(source='actor.id')
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_id', 'verb', 'target_object_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'actor', 'timestamp']