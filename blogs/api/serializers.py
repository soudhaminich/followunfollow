from rest_framework.serializers import(
    HyperlinkedIdentityField,
    ModelSerializer,
    RelatedField,
    CharField,
    ImageField,
    SerializerMethodField
)

from blogs.models import Post
from comments.models import Comment
from comments.api.serializers import CommentSerializer


class PostDetailSerializer(ModelSerializer):
    username = CharField(source='author.username', read_only=True)
    author_image = ImageField(
        source='author.profile.image', read_only=True)
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments
