import json
import requests
import os
import uuid
from pathlib import Path
from django.conf import settings
from django.core.files.base import ContentFile
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import re
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from PIL import Image
import random
from django.core.files import File
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class AuthorInfo(BaseModel):
    author_info: str
    author_works: str

def clean_gpt_json_response(raw_text: str) -> str:
    cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw_text.strip(), flags=re.MULTILINE)
    return cleaned

def query_gpt_for_author_info(name: str) -> tuple[str, str]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = (
        f"당신은 작가 정보를 요약해주는 AI입니다. 사용자가 작가 정보를 주면 다음과 같은 JSON을 반환하세요.\n\n"
        f"- 'author_info': 작가의 국적, 활동 분야, 대표 경력 등을 포함한 다섯 줄 소개\n"
        f"- 'author_works': 작가의 대표 작품 3~5개를 콤마로 구분한 문자열, 정보의 도서를 쓰지 말고 다른 작품을 3개 이상 넣기, 없는 도서를 만들어서 넣지 마세요.\n\n"
        f"작가이름: {name}\n"
        f"출력 예시:\n"
        f"{{\n  \"author_info\": \"...\",\n  \"author_works\": \"작품1, 작품2, 작품3\"\n}}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "사용자 요청에 따라 작가 정보 JSON을 생성하세요."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        raw = response.choices[0].message.content
        cleaned = clean_gpt_json_response(raw)
        data = json.loads(cleaned)
        return (
            data.get("author_info", "작가 정보를 가져오지 못했습니다."),
            data.get("author_works", "대표작 정보를 가져오지 못했습니다.")
        )
    except Exception as e:
        print("⚠️ GPT 오류:", e)
        return (
            "작가 정보를 가져오지 못했습니다.",
            "대표작 정보를 가져오지 못했습니다."
        )

def process_author_info_from_ai(prompt, name: str, title: Optional[str] = None) -> tuple[str, str, Optional[ContentFile]]:
    info_text, works_text = query_gpt_for_author_info(prompt)

    return info_text, works_text
