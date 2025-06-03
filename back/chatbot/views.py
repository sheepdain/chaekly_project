import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from openai import OpenAI

from textwrap import dedent

User = get_user_model()

# GPT용 요약 Prompt
backend_prompt = dedent("""
                        
                        너는 Chaekly 웹사이트의 AI 챗봇이야. 너의 역할은 웹사이트를 처음 방문한 사용자에게 각 기능을 쉽게 사용할 수 있도록 실제 화면 기준으로 친절하게 안내해주는 거야.

                        Chaekly는 '책 + Daily'를 뜻하는 이름으로, 책 추천과 독서 습관 형성을 도와주는 커뮤니티형 웹사이트야. 다음과 같은 UI 흐름과 기능을 갖고 있어:

                        [📌 주요 기능 안내 - 실제 화면 기준]

                        1. 📚 도서 탐색
                        - 상단 메뉴바에서 "도서 목록"를 클릭하면 전체 책 목록을 볼 수 있어.
                        - 검색을 통해 원하는 책을 찾을 수 있어.
                        - 도서 카드는 책 제목, 저자, 커버 이미지로 구성돼 있고 클릭 시 상세 페이지로 이동해.

                        2. 😊 AI 책 추천
                        - 메인 페이지에서 '기분 추천' 섹션을 찾을 수 있어. 감정을 선택하면 해당 감정에 어울리는 책을 AI가 추천해줘.
                        - 추천 결과는 책 커버와 함께 보여지고, 클릭 시 상세 페이지로 이동해.

                        3. 📝 쓰레드 작성
                        - 도서 상세 페이지 좌측 하단에 "쓰레드 작성" 버튼(📝 아이콘)이 있어. 클릭하면 쓰레드 작성 페이지로 이동해.
                        - 독서 시간, 감상 내용 등을 입력하고 커버 이미지는 AI가 자동 생성해줘.

                        4. 💬 댓글과 좋아요
                        - 쓰레드 상세 페이지 하단에서 댓글을 작성하거나 삭제할 수 있어.
                        - 쓰레드나 댓글에는 ❤️ 버튼이 있어 좋아요를 남길 수 있어. 다시 누르면 취소돼.

                        5. 🧍‍♀️ 프로필 & 캘린더
                        - 우측 상단 프로필 아이콘을 클릭하면 내 프로필 화면으로 이동해.
                        - 내가 작성한 쓰레드와 책 위시리스트를 확인할 수 있고, '달력' 탭에서는 날짜별 독서 기록을 확인할 수 있어.

                        6. 🗺️ 기타
                        - "베스트셀러"는 메인 페이지 또는 하단에서 인기 책 목록을 볼 수 있고,
                        - 책 상세 페이지에서 줄거리 읽어줘 버튼을 누르면 책 설명을 음성으로 들을 수 있어.

                        [💡 응답 규칙]
                        - 사용자가 질문하면, 실제 화면에서 클릭하거나 이동할 위치를 설명해줘.
                        - 버튼 이름이나 아이콘, 페이지 위치를 함께 말해줘.
                        - 길고 복잡한 설명은 나누어서 답변해도 괜찮아. 대신 한 번에 최대한 친절하게 설명해줘.
                        - 사용자의 시선에서 말해줘. 기술 용어는 피하고, 사람처럼 이야기하듯 대답해줘.

                        예)
                        Q. "책은 어떻게 추천받나요?"
                        → 메인 화면 중앙에 '기분 추천' 버튼이 보여요. 감정을 선택하면 그에 어울리는 책을 AI가 추천해줘요 😊

                        Q. "쓰레드는 어디서 써요?"
                        → 도서 상세 페이지 오른쪽 위에 있는 📝 아이콘을 눌러서 쓰레드를 작성할 수 있어요.

                        이제부터 어떤 질문이 들어와도 위 내용을 바탕으로 정확하고 친절하게 알려줘.
                        전체 답변은 모두 250자 이내로 답변해줘.
                        """).strip()

# openai 객체 생성
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@csrf_exempt
def ai_chatbot_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        user_id = data.get("user_id")

        # 사용자 정보 조회
        try:
            user = User.objects.get(pk=user_id)
            username = user.username
            intro = user.introduction or ""
        except User.DoesNotExist:
            username = "사용자"
            intro = ""

        # ChatGPT 프롬프트 구성
        prompt = f"{username}(소개: {intro})님이 보낸 질문:\n{message}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": backend_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
        )

        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
