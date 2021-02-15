from rest_framework.serializers import(
    HyperlinkedIdentityField,
    ModelSerializer,
    RelatedField,
    CharField,
    ImageField,
    SerializerMethodField
)

from support.models import Question
from comments.models import Comment
from comments.api.serializers import CommentSerializer


class QuestionSerializer(ModelSerializer):
    comments = SerializerMethodField()
    username = CharField(source='user.username', read_only=True)
    user_image = ImageField(
        source='user.profile.image', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        lookup_field = 'slug'

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments
