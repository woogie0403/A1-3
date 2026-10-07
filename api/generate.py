# ==========================================================================
# 여기로 (Yeogiro) - AI 여행 코스 생성 백엔드
# Vercel Serverless Function (Python) + Google Gemini API
# ==========================================================================
from http.server import BaseHTTPRequestHandler
import json
import os
import requests

GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-latest",
]


def build_prompt(dest, duration, companion, transport, theme):
    """사용자 입력을 바탕으로 Gemini에게 보낼 지시문(프롬프트)을 만든다."""
    # 기간별 스팟 수 및 일차 규칙 정의
    if "2박 3일" in duration:
        duration_rule = """- 선택된 기간은 '2박 3일'입니다.
- 반드시 '1일차', '2일차', '3일차' 3개 일차로 나누어 총 8~10개의 스팟을 timeline에 포함하세요.
  * 1일차: 도착 후 코스 3개 (오후 관광, 카페, 저녁/야경)
  * 2일차: 풀코스 3~4개 (오전 관광, 점심 맛집, 오후 핫플, 저녁 명소)
  * 3일차: 귀가 전 코스 2~3개 (오전 산책, 브런치/점심 맛집, 귀가 전 카페)"""
    elif "1박 2일" in duration:
        duration_rule = """- 선택된 기간은 '1박 2일'입니다.
- 반드시 '1일차'와 '2일차' 2개 일차로 나누어 총 6~8개의 스팟을 timeline에 포함하세요.
  * 1일차: 1일차 코스 3~4개 (오전/오후 관광, 점심 맛집, 카페, 저녁/야경)
  * 2일차: 2일차 코스 3~4개 (오전 힐링 관광, 점심 로컬 맛집, 감성 카페/베이커리)"""
    else:
        duration_rule = """- 선택된 기간은 '당일치기'입니다.
- '1일차' 단일 일정으로 총 4개의 핵심 스팟(오전 관광, 점심 맛집, 오후 카페/액티비티, 저녁 식사/야경)으로 구성하세요."""

    return f"""당신은 대한민국 국내 여행 전문 AI 플래너 '여기로(Yeogiro)'입니다.
아래 조건에 맞춰 네이버 지도와 카카오맵에 실제로 존재하는 진짜 유명 핫플 중심의 현실적인 국내 여행 코스를 설계하세요.

[여행 조건]
- 여행지: {dest}
- 기간: {duration}
- 동행자: {companion}
- 이동수단: {transport}
- 테마: {theme}

[★ 일정 기간({duration}) 필수 규칙]
{duration_rule}
- timeline 배열의 모든 항목에는 해당 스팟이 속한 일차를 "day" 필드("1일차", "2일차", "3일차")로 반드시 표기하세요.

[★ 엄격한 핵심 원칙 - 가짜/환각 상호명 생성 절대 금지]
1. 가상의 식당, 카페, 장소 이름을 절대로 지어내지 마세요.
2. 식당(맛집)과 카페는 네이버 지도, 카카오맵, 블루리본 서베이 등에 실제로 등록되어 있고 리뷰가 많은 실존 대표 유명 상호명(예: 부산의 경우 '초량밀면', '이재모피자 본점', '쌍둥이돼지국밥', '해운대 암소갈비집' 등)만 정확하게 사용하세요.
3. [동선 현실성]: 각 일차 내의 스팟들은 완전히 다른 먼 지역으로 튀지 않고, {dest} 내에서 같은 권역(예: 1일차는 해운대·기장권, 2일차는 영도·남포권 등)으로 묶어 실제 차량/도보 10~15분 이내로 이어지도록 설계하세요.
4. 이동수단({transport})과 동행자({companion})의 특성을 세심하게 반영하세요.
5. 1인 기준 예상 경비(식비+카페+입장료+숙박참고)를 {duration} 전체 일정에 맞게 현실적인 원화 범위(예: 1박 2일 기준 약 90,000원 ~ 140,000원)로 제시하세요.

[출력 형식]
반드시 아래 JSON 스키마 그대로만 응답하세요. 설명 문장이나 마크다운(```)은 절대 넣지 마세요.
{{
  "title": "코스 제목 (예: 부산 영도·해운대 1박 2일 로컬 미식 코스)",
  "summary": "감성적인 한 줄 요약",
  "theme_tag": "{theme}",
  "budget": "약 00,000원 ~ 00,000원 (전체 일정 1인 기준)",
  "timeline": [
    {{
      "day": "1일차",
      "time": "오전 10:30",
      "name": "실제 관광지 이름",
      "category": "관광",
      "distance": "출발지에서 바로",
      "description": "이 장소에 대한 1~2문장 설명",
      "menu": "",
      "photo": "사진 꿀팁"
    }},
    {{
      "day": "1일차",
      "time": "오후 12:30",
      "name": "실제 유명 맛집 상호명",
      "category": "맛집",
      "distance": "직전 스팟에서 도보 7분",
      "description": "실제 맛집 특징 설명",
      "menu": "실제 대표 시그니처 메뉴 이름",
      "photo": ""
    }},
    {{
      "day": "1일차",
      "time": "오후 15:00",
      "name": "실제 유명 카페 상호명",
      "category": "카페",
      "distance": "직전 스팟에서 차로 5분",
      "description": "카페 특징 설명",
      "menu": "시그니처 메뉴",
      "photo": "포토존 팁"
    }},
    {{
      "day": "1일차",
      "time": "오후 19:00",
      "name": "실제 저녁 맛집/야경",
      "category": "저녁",
      "distance": "직전 스팟에서 차로 10분",
      "description": "설명",
      "menu": "대표 메뉴",
      "photo": "야경 팁"
    }},
    {{
      "day": "2일차",
      "time": "오전 10:30",
      "name": "2일차 실제 관광지/산책",
      "category": "관광",
      "distance": "숙소에서 차로 10분",
      "description": "설명",
      "menu": "",
      "photo": "포토 팁"
    }}
  ],
  "tips": "주차/웨이팅/예약/꿀팁 등 실제 현지 방문 시 유용한 팁 1~2가지"
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
            "temperature": 0.2,
        },
    }

    last_error = None
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        try:
            resp = requests.post(url, params={"key": api_key}, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                return json.loads(text.strip())
            else:
                last_error = f"{model_name} HTTP {resp.status_code}: {resp.text}"
                continue
        except requests.exceptions.Timeout:
            last_error = f"{model_name} Timeout"
            continue
        except requests.exceptions.RequestException as e:
            last_error = f"{model_name} RequestException: {e}"
            continue

    raise requests.exceptions.RequestException(f"모든 AI 모델 호출 실패: {last_error}")



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

    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("[테스트] '제주도 / 1박 2일 / 연인 / 렌트카 / 힐링' 코스를 생성합니다...\n")
    sample = generate_course("제주도", "1박 2일", "연인·데이트", "🚗 렌트카/자차", "🌿 힐링·자연")
    print(json.dumps(sample, ensure_ascii=False, indent=2))

