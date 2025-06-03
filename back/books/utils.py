import os
import re
import json
import requests
from openai import OpenAI
from datetime import datetime
from .models import Book, CustomCategory
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 알라딘 API 설정
ALADIN_API_URL = 'https://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
ALADIN_API_KEY = os.getenv('ALADIN_API_KEY')

# OpenAI API 키 설정
client = OpenAI(api_key=OPENAI_API_KEY)

def clean_json_block(text):
    # ```json ... ``` 같은 마크다운 제거
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())


def fetch_titles_from_ai(mood, n=3):
    prompt = (
        f"당신은 대한민국 온라인 서점의 전문 도서 큐레이터입니다.\n"
        f"아래 요구 조건을 충족하며, 사용자의 기분({mood})에 어울리는 실제 한국 도서 제목을 최대 {n}권 추천해 주세요.\n"
        f"---\n"
        f"[요구 조건]\n"
        f"1. 반드시 알라딘, 교보문고, 예스24 등 주요 서점에서 검색 가능한 도서만 포함할 것.\n"
        f"2. 허구의 책 제목을 만들지 말 것.\n"
        f"3. 추천 전, 각 도서가 실제 존재하는지 검색했다고 가정할 것.\n"
        f"4. 아래 예시와 동일하게 반드시 JSON 배열(책 제목만 포함, 부가 설명 없이)로만 답변할 것.\n"
        f"5. 조건을 만족하는 도서가 없다면 빈 배열([])을 출력할 것.\n"
        f"6. 예시 외에 불필요한 텍스트(설명, 안내 등)는 절대 포함하지 말 것.\n"
        f"[예시]\n"
        f"[\"아몬드\", \"82년생 김지영\", \"여행의 이유\"]\n"
        f"---\n"
        f"사용자 기분: {mood}\n"
        f"(현재 시간: {datetime.now().isoformat()})"
    )
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.2,
        )
        text = res.choices[0].message.content.strip()
        print("[GPT 응답 원문]", text)
        cleaned = clean_json_block(text)
        return json.loads(cleaned)
    except Exception as e:
        print("[OpenAI 오류]", e)
        return []


# 2. 알라딘에서 검색해서 DB에 저장
def fetch_and_save_books(titles):
    saved = []

    for title in titles:
        print(f"알라딘 검색: {title}")

        params = {
            'ttbkey': ALADIN_API_KEY,
            'Query': title,
            'QueryType': 'Keyword',  
            'MaxResults': 5, 
            'Cover': 'Big',
            'Output': 'js',
            'Version': '20131101'
        }
        resp = requests.get(ALADIN_API_URL, params=params)
        print("[알라딘 응답]", resp.text)
        data = resp.json()
        items = data.get("item", [])
        print("[파싱된 아이템]", items)
        if not items:
            print(f"❌ '{title}' 검색 결과 없음")
            continue

        item = next((i for i in items if title in i.get("title", "")), items[0])
        print(item)

        isbn13 = item.get('isbn13')
        try:
            pub_date = datetime.strptime(item.get('pubDate', ''), "%Y-%m-%d").date()
        except:
            pub_date = datetime.today().date()

        # 카테고리 중분류 추출
        category_full = item.get('categoryName', '')
        parts = [p.strip() for p in category_full.split('>')]
        category_mid = parts[1] if len(parts) > 1 else parts[0]
        cat_obj, _ = CustomCategory.objects.get_or_create(name=category_mid)

        # Book 저장 (중복 방지)
        book, _ = Book.objects.update_or_create(
            isbn13=isbn13,
            defaults={
                'title': item.get('title', '')[:200],
                'author': item.get('author', ''),
                'publisher': item.get('publisher', ''),
                'pub_date': pub_date,
                'description': item.get('description', ''),
                'category_id': item.get('categoryId', 0),
                'category_name': category_full,
                'cover': item.get('cover', ''),
                'link': item.get('link', ''),
                'custom_category': cat_obj,
                'customer_review_rank': item.get('customerReviewRank', 0),
                'best_duration': item.get('bestDuration', ''),
                'best_rank': item.get('bestRank', 0),
            }
        )
        saved.append(book)


    return saved