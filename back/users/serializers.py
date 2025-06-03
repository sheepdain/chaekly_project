from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class BookSimpleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('id', 'title', 'cover')

    class UserSimpleSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "username", "nickname")

    threads = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    wishlist = BookSimpleSerializer(many=True)
    followers = UserSimpleSerializer(many=True, read_only=True)
    is_follow = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'age', 'email',
                  'profile_image', 'introduction', 'followers',
                  'threads', 'comments', 'wishlist', 'is_follow',
                  'followers_count', 'following_count',)

    def get_threads(self, obj):
        from threads.serializers import ThreadListSerializer
        from threads.models import Thread
        from django.db.models import Count

        threads = Thread.objects.filter(user=obj).annotate(
            like_count=Count('like_users', distinct=True),
            comment_count=Count('comments', distinct=True)
        ).order_by('-created_at')
        return ThreadListSerializer(threads, many=True, context=self.context).data

    def get_comments(self, obj):
        from threads.serializers import CommentSerializer
        comments = obj.comments.all().order_by('-created_at')
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def get_is_follow(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return False
        user = request.user
        if user.is_authenticated:
            return obj.followers.filter(id=user.id).exists()
        return False

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()




class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': '이메일을 입력해 주세요.',
            'invalid': '유효한 이메일 주소를 입력해 주세요.'
        }
    )
    nickname = serializers.CharField(
        required=True,
        max_length=15,
        error_messages={
            'required': '닉네임을 입력해 주세요.',
            'max_length': '닉네임은 최대 15자까지 가능합니다.'
        }
    )
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')],
        required=True,
        error_messages={
            'required': '성별을 선택해 주세요.',
            'invalid_choice': '유효한 성별을 선택해 주세요.'
        }
    )
    age = serializers.IntegerField(
        required=True,
        min_value=0,
        error_messages={
            'required': '나이를 입력해 주세요.',
            'min_value': '나이는 0 이상의 숫자여야 합니다.',
            'invalid': '숫자를 입력해 주세요.'
        }
    )
    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid_image': '이미지 파일만 업로드할 수 있습니다.'
        }
    )
    introduction = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        error_messages={
            'max_length': '소개글은 500자 이내로 작성해 주세요.'
        }
    )

    class Meta:
        model = User
        fields = (
            "email",
            "nickname",
            "gender",
            "age",
            "profile_image",
            "introduction",
        )

    def validate_nickname(self, value):
        user = self.instance
        stripped = value.strip()
        if all('\u3131' <= char <= '\u314E' or '\u314F' <= char <= '\u3163' for char in stripped):
            raise serializers.ValidationError('사용할 수 없는 닉네임입니다.')
        # 본인 닉네임은 허용, 타인과 겹치면 에러
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError('이미 사용 중인 닉네임입니다.')
        return value

    def validate_email(self, value):
        user = self.instance
        # 본인 이메일은 허용, 타인과 겹치면 에러
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.save()
        return instance



# 이 아래는 Thread, Comment 시리얼라이저에서 사용
class UserOfThreadSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField()
    nickname = serializers.CharField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_follow = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "username", "nickname", "profile_image",
            "followers_count", "following_count", "is_follow", "followers"
        )

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_follow(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.followers.filter(id=user.id).exists()
        return False

    def get_followers(self, obj):
        # 원하는 간단 정보만 추출
        return [
            {
                "id": u.id,
                "nickname": u.nickname,
                "profile_image": u.profile_image.url if u.profile_image else None
            }
            for u in obj.followers.all()
        ]


class UserOfCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname',)