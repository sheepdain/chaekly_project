from rest_framework import serializers
from .models import Book, CustomCategory, Author

class AuthorSerializer(serializers.ModelSerializer):
    author_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['name', 'profile_img', 'info', 'works', 'author_image_url']

    def get_author_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_img and hasattr(obj.profile_img, 'url'):
            return request.build_absolute_uri(obj.profile_img.url) if request else obj.profile_img.url
        return None  # ❗ 실패하면 None 반환

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id', 'title', 'author', 'publisher',
                'description', 'cover',
                'customer_review_rank', 'best_rank',)


class CustomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCategory
        fields = ('id', 'name',)

class BookSerializer(serializers.ModelSerializer):
    custom_category = CustomCategorySerializer(read_only=True)
    wishlisted_users = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    class Meta:
        model = Book
        fields = '__all__'



# 쓰레드 조회 시 보여줄 책 정보가 담긴 시리얼라이저
class BookSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover',)