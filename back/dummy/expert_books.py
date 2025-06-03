import os
import django
import json

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booknest.settings")  # settings.py 경로에 맞게 수정
django.setup()

from books.models import Book

def convert_dates(obj):
    for entry in obj:
        for key, value in entry.items():
            if hasattr(value, 'isoformat'):
                entry[key] = value.isoformat()
    return obj

def export_books():
    data = list(Book.objects.all().values())
    data = convert_dates(data)
    with open("books_final_utf8bom.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ books_final_utf8bom.json 저장 완료")

if __name__ == "__main__":
    export_books()
