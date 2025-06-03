from rest_framework import serializers
from users.serializers import UserOfThreadSerializer, UserOfCommentSerializer
from books.serializers import BookSummarySerializer
from .models import Thread, Comment


#책에 작성된 쓰레드 조회
class ThreadListOfBookSerializer(serializers.ModelSerializer):
    user = UserOfThreadSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'user', 'book', 'title', 'cover',
                'is_public', 'created_at','like_count',
                'comment_count',)
        read_only_fields = ('user', 'book',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserOfCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'thread',)


class ThreadSerializer(serializers.ModelSerializer):
    user = UserOfThreadSerializer(read_only=True)
    book = BookSummarySerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    is_liked = serializers.SerializerMethodField()

    comments = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = (
            'id', 'user', 'book', 'reading_time', 'read_date', 'title',
            'content', 'is_public', 'created_at', 'updated_at', 'cover',
            'like_users', 'like_count', 'comments', 'comment_count', 'is_liked',
        )
        read_only_fields = ('user', 'book', 'like_count', 'like_users')

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.order_by('created_at'), many=True).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like_users.all()
        return False

class ThreadListSerializer(serializers.ModelSerializer):
    user = UserOfThreadSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'user', 'title', 'cover',
                  'is_public', 'created_at',
                  'like_count', 'comment_count')
        read_only_fields = ('user',)


