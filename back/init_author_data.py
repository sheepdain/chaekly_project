# import os
# import django
# import time
# import re

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booknest.settings')  # ✔ 반드시 이 경로로!
# django.setup()

# from django.core.files.base import ContentFile
# from books.models import Book, Author
# from books.utils2 import process_author_info_from_ai

# books = Book.objects.all()
# total = books.count()
# processed = 0

# for book in books:
#     full_name = book.author.strip()
#     author, _ = Author.objects.get_or_create(name=full_name)

#     if not author.info or not author.works or not author.profile_img:
#         print(f"📘 [{processed+1}/{total}] 처리 중: {book.title} / {full_name}")
#         prompt = f"책 제목: {book.title}\n출판사: {book.publisher}\n도서 설명: {book.description or '설명 없음'}"

#         info_text, works_text, image_url = process_author_info_from_ai(prompt, full_name)

#         author.info = info_text
#         author.works = works_text

#         # if isinstance(image_url, ContentFile):
#         #     author.profile_img.save(image_url.name, image_url, save=False)
#         # elif isinstance(image_url, str) and image_url.startswith('/static/'):
#         #     author.profile_img.name = image_url.replace('/static/', '')
#         if isinstance(image_url, ContentFile):
#             if not author.profile_img or not author.profile_img.name.startswith("default_"):
#                 author.profile_img.save(image_url.name, image_url, save=False)

#         elif isinstance(image_url, str) and image_url.startswith('/static/'):
#             author.profile_img.name = image_url.replace('/static/', '')


#         author.save()
#         time.sleep(1)

#     else:
#         print(f"✅ [{processed+1}/{total}] 스킵: {full_name} (이미 정보 있음)")
    
#     processed += 1

# print("✅ 모든 작가 정보 수집 완료!")




# init_author_data.py
import sys
import os

# ✅ 1. 경로 먼저 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ 2. settings 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booknest.settings')

# ✅ 3. Django 초기화
import django
django.setup()

# ✅ 4. setup 이후에 import
from django.core.files.base import ContentFile
from books.models import Book, Author
from books.utils2 import process_author_info_from_ai


def populate_authors():
    books = Book.objects.filter(id__gte=570)
    for book in books:
        full_name = book.author.strip()
        author, created = Author.objects.get_or_create(name=full_name)

        if author.info and author.works:
            continue

        print(f"처리 중: {book.title} - {book.author}")

        prompt = f"책 제목: {book.title}\n출판사: {book.publisher}\n도서 설명: {book.description}\n지은이: {book.author}"
        info, works, image_file = process_author_info_from_ai(prompt, full_name, book.title)

        author.info = info
        author.works = works
        if image_file and isinstance(image_file, ContentFile):
            author.profile_img.save(image_file.name, image_file, save=False)

        author.save()

    print("✅ 모든 작가 정보 갱신 완료")


if __name__ == '__main__':
    populate_authors()
