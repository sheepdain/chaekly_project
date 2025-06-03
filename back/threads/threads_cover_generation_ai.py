import openai, slugify, json, os, requests
from typing import Dict
from django.core.files.base import ContentFile
from datetime import datetime

def save_image_to_thread_cover(url, thread_instance):
    response = requests.get(url)
    if response.status_code == 200:
        safe_title = slugify.slugify(thread_instance.title)[:20]
        today = datetime.now().strftime('%Y%m%d')
        file_name = f"thread_{thread_instance.id}_{safe_title}_{today}.jpg"
        thread_instance.cover.save(file_name, ContentFile(response.content), save=True)


def is_thread_insufficient(thread_title: str, thread_content: str) -> bool:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "다음은 사용자의 책 감상 쓰레드입니다. "
                    "내용이 너무 짧거나, 의미 있는 시각적 장면을 유도하기 어려울 정도로 빈약하면 "
                    '반드시 JSON 형식으로 {"result": true} 또는 {"result": false} 중 하나를 반환하세요. 이유는 설명하지 마세요.'
                )
            },
            {
                "role": "user",
                "content": f"제목: {thread_title}\n내용: {thread_content}"
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=5,
        temperature=0,
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("result", False)


def generate_image(thread_title: str, thread_content: str, book_title: str, book_description: str) -> Dict:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # ✅ 쓰레드 부실 여부 평가
    if is_thread_insufficient(thread_title, thread_content):
        thread_content += f"\n\n[보완 정보: 책 설명]\n{book_description.strip()[:1000]}"

    # 1. GPT-4o-mini를 이용한 콘텐츠 분석
    chat_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""
                아래는 사용자가 작성한 독서 쓰레드입니다.

                이 쓰레드의 제목과 내용을 바탕으로 시각적으로 떠오르는 장면을 분석하고, 아래 형식의 JSON으로 응답하세요.

                도서 제목: 『{book_title}』 (참고용입니다. 시각적 장면은 아래 쓰레드 기준으로 작성하세요)

                쓰레드 제목: {thread_title}

                쓰레드 내용:
                {thread_content[:2000]}

                출력 형식 (예시):
                {{
                "style_anchor": "...",          # 그림의 스타일 예: 지브리 수채화, 픽셀 아트 등
                "main_description": "...",      # 쓰레드 내용을 시각화한 핵심 장면 묘사
                "negative_prompt": "...",       # 피해야 할 요소들 예: 텍스트, 워터마크 등
                "mood": "..."                   # 분위기 예: calm, vibrant 등
                }}

                ※ 주의: 위 예시는 형식만 참고하십시오. 내용은 쓰레드에 기반하여 새로 작성되어야 하며, 복사하지 마세요.
                """

            },
            {
            "role": "user",
            "content": f"제목: {thread_title}\n내용: {thread_content[:2000]}"
        }
        ],
        response_format={"type": "json_object"},
        max_tokens=256,
        temperature=1,
    )
    analysis = json.loads(chat_response.choices[0].message.content)

    # 2. 프롬프트 최적화
    prompt = (
        f"스타일: {analysis['style_anchor']}, "
        f"장면 설명: {analysis['main_description']}, "
        f"부정적 요소: {analysis['negative_prompt']}, "
        f"분위기: {analysis['mood']}, "
        f"기술적 사양: 8K UHD, 세밀한 질감"
    )[:1000]

    # 3. DALL·E 3로 이미지 생성 (최신 방식)
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="hd",
        style="vivid" if analysis.get('mood') == "vibrant" else "natural",
    )

    return {
        "url": image_response.data[0].url,
        "analysis": analysis,
    }
