# ==========================================================================
# 여기로 (Yeogiro) - AI 여행 코스 생성 백엔드
# Vercel Serverless Function (Python) + Google Gemini API
# ==========================================================================
from http.server import BaseHTTPRequestHandler
import json
import os
import requests

GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def build_prompt(dest, duration, companion, transport, theme):
    """사용자 입력을 바탕으로 Gemini에게 보낼 지시문(프롬프트)을 만든다."""
    return f"""당신은 대한민국 국내 여행 전문 AI 플래너 '여기로(Yeogiro)'입니다.
아래 조건에 맞춰 '동선 낭비 없는' 현실적인 국내 여행 코스를 설계하세요.

[여행 조건]
- 여행지: {dest}
- 기간: {duration}
- 동행자: {companion}
- 이동수단: {transport}
- 테마: {theme}

[설계 규칙]
1. 하루 4개의 핵심 스팟으로 구성한다: (1) 오전 관광/산책 명소, (2) 점심 로컬 맛집, (3) 오후 감성 카페 또는 액티비티, (4) 저녁 식사 및 야경/선셋 명소.
2. 모든 식당과 카페는 반드시 '직전 스팟'에서 도보/차량 10분 이내로 배치한다.
3. 이동수단({transport})과 동행자({companion})의 특성을 코스에 반영한다.
4. 반드시 실제 존재하는 {dest}의 지명/장소를 사용한다.
5. 1인 기준 예상 경비(식비+카페+입장료)를 현실적인 원화 범위로 제시한다.

[출력 형식]
반드시 아래 JSON 스키마 그대로만 응답하세요. 설명 문장이나 마크다운(```)은 절대 넣지 마세요.
{{
  "title": "코스 제목 (예: 제주 서쪽 감성 힐링 코스)",
  "summary": "감성적인 한 줄 요약",
  "theme_tag": "{theme}",
  "budget": "약 00,000원 ~ 00,000원",
  "timeline": [
    {{
      "time": "오전 10:00",
      "name": "스팟 이름",
      "category": "관광",
      "distance": "출발지에서 바로",
      "description": "이 장소에 대한 1~2문장 설명",
      "menu": "",
      "photo": "사진이 잘 나오는 앵글/시간대 팁"
    }},
    {{
      "time": "오후 12:30",
      "name": "맛집 이름",
      "category": "맛집",
      "distance": "직전 스팟에서 7분",
      "description": "맛집 설명",
      "menu": "대표 메뉴",
      "photo": ""
    }},
    {{
      "time": "오후 15:00",
      "name": "카페/액티비티 이름",
      "category": "카페",
      "distance": "직전 스팟에서 5분",
      "description": "설명",
      "menu": "시그니처 메뉴 (카페일 경우)",
      "photo": "포토 팁"
    }},
    {{
      "time": "오후 19:00",
      "name": "저녁/야경 명소",
      "category": "저녁",
      "distance": "직전 스팟에서 10분",
      "description": "설명",
      "menu": "대표 메뉴",
      "photo": "야경/선셋 촬영 팁"
    }}
  ],
  "tips": "주차/웨이팅/예약 등 현지인만 아는 시크릿 꿀팁 1~2가지"
}}"""


def generate_course(dest, duration, companion, transport, theme):
    """Gemini API를 호출해 여행 코스 JSON(dict)을 반환한다."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    payload = {
        "contents": [{"parts": [{"text": build_prompt(dest, duration, companion, transport, theme)}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.9,
        },
    }

    resp = requests.post(GEMINI_URL, params={"key": api_key}, json=payload, timeout=25)
    resp.raise_for_status()

    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


class handler(BaseHTTPRequestHandler):
    """Vercel이 /api/generate 요청을 받으면 실행하는 핸들러."""

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            params = json.loads(body.decode("utf-8"))

            dest = (params.get("destination") or "").strip()
            if not dest:
                self._send(400, {"error": "여행지를 입력해 주세요."})
                return

            result = generate_course(
                dest,
                params.get("duration", "1박 2일"),
                params.get("companion", "연인·데이트"),
                params.get("transport", "🚗 렌트카/자차"),
                params.get("theme", "🌿 힐링·자연"),
            )
            self._send(200, result)

        except requests.exceptions.Timeout:
            self._send(504, {"error": "AI 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요."})
        except requests.exceptions.RequestException:
            self._send(502, {"error": "AI 서버와 통신 중 오류가 발생했습니다."})
        except Exception as e:
            self._send(500, {"error": "코스 생성 중 오류가 발생했습니다.", "detail": str(e)})

    def _send(self, status, data):
        """상태 코드와 JSON 본문을 응답으로 내보내는 헬퍼."""
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))


# --- 로컬 단독 테스트용 -----------------------------------------------------
# 터미널에서  python api/generate.py  를 실행하면 실제 AI 호출을 검증한다.
if __name__ == "__main__":
    import pathlib

    # 상위 폴더의 .env 파일을 수동으로 읽어 환경변수로 등록
    env_path = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    print("[테스트] '제주도 / 1박 2일 / 연인 / 렌트카 / 힐링' 코스를 생성합니다...\n")
    sample = generate_course("제주도", "1박 2일", "연인·데이트", "🚗 렌트카/자차", "🌿 힐링·자연")
    print(json.dumps(sample, ensure_ascii=False, indent=2))
