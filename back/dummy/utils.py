import requests
from datetime import datetime
from .models import Book, CustomCategory  # Category 모델 import

def fetch_popular_books(max_results=100):
    API_KEY = 'ttbekdls51231404001'
    url = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'

    total_saved = 0

    params = {
        'ttbkey': API_KEY,
        'QueryType': 'ItemNewAll',
        'MaxResults': max_results,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101',
        'Cover': 'Big'
    }

    response = requests.get(url, params=params)
    data = response.json()

    count = 0
    for item in data.get('item', []):
        try:
            pub_date = datetime.strptime(item.get('pubDate', ''), "%Y-%m-%d").date()
        except:
            pub_date = datetime.today().date()

        category_name_full = item.get('categoryName', '')  # 전체 경로
        cat_parts = [p.strip() for p in category_name_full.split('>')]  # 공백 없애기
        category_mid = cat_parts[1] if len(cat_parts) > 1 else cat_parts[0]

        # 중복 없이 Category 저장
        category_obj, _ = CustomCategory.objects.get_or_create(name=category_mid)

        # Book 저장 (category 연결 포함)
        _, created = Book.objects.update_or_create(
            isbn13=item.get('isbn13'),
            defaults={
                'title': item.get('title', ''),
                'author': item.get('author', ''),
                'publisher': item.get('publisher', ''),
                'pub_date': pub_date,
                'description': item.get('description', ''),
                'category_id': item.get('categoryId', 0),
                'category_name': category_name_full,
                'cover': item.get('cover', ''),
                'link': item.get('link', ''),
                'custom_category': category_obj,  # ForeignKey 연결
            }
        )
        if created:
            count += 1

    print(f'{count}권 저장 완료')
