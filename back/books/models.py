from django.db import models

# Create your models here.
class CustomCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)  # 도서명
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()  # 출간일
    isbn13 = models.CharField(max_length=13)
    description = models.TextField(blank=True)  # 책 소개
    category_id = models.IntegerField()  # 알라딘 CategoryId (API 기준)
    category_name = models.CharField(max_length=50)  # API에서 같이 주어지는 경우
    cover = models.URLField()  # 표지 이미지
    link = models.URLField()  # 알라딘 상세 페이지 링크
    # 소분류 카테고리(1Depth)
    custom_category = models.ForeignKey(CustomCategory, on_delete=models.SET_NULL, null=True)
    customer_review_rank=models.FloatField(blank=True)
    best_duration=models.TextField(blank=True)
    best_rank=models.IntegerField(blank=True)


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    profile_img = models.ImageField(
        upload_to='author_profiles/',
        null=True, blank=True
    )
    info = models.TextField(null=True, blank=True) 
    # works : 작가 대표작
    works = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name
