from pathlib import Path
from gtts import gTTS
from django.conf import settings

def generate_description_tts(book):
    """
    도서 설명(description)을 mp3로 생성하고 파일 경로 반환
    """
    if not book.description:
        return None
    
    file_name = f"description_{book.pk}.mp3"
    rel_path = Path("tts") / file_name
    abs_path = Path(settings.MEDIA_ROOT) / rel_path

    # 파일이 이미 존재한다면 패스
    if abs_path.exists():
        return str(rel_path)

    try:
        tts = gTTS(book.description, lang='ko')
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(abs_path))
        return str(rel_path)
    except Exception as e:
        print("TTS 생성 실패:", e)
        return None
