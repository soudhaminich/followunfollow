from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    CharField,
    ImageField
)
from comments.models import Comment
User = settings.AUTH_USER_MODEL


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class CommentChildSerializer(ModelSerializer):
    # user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'comment',
            'timestamp',
        ]


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    replies = SerializerMethodField()
    username = CharField(source='user.username', read_only=True)
    user_image = ImageField(
        source='user.profile.image', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'comment',
            'reply_count',
            'replies',
            'timestamp',
            'username',
            'user_image'
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None
