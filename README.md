# ✈️ 여기로 (Yeogiro) — AI 1분 국내 여행 코스 플래너

> 국내 여행지와 취향만 고르면, AI가 동선 밀착형 맛집과 포토존까지 1분 만에 스케치합니다.  

[![배포 상태](https://img.shields.io/badge/배포-Vercel_Live-black?style=flat-square&logo=vercel)](https://a1-3-cyan.vercel.app/)
![AI 모델](https://img.shields.io/badge/AI-Google_Gemini-blue?style=flat-square&logo=google)
![프론트엔드](https://img.shields.io/badge/Frontend-Vanilla_JS-yellow?style=flat-square&logo=javascript)

🔗 **라이브 배포 웹 서비스**: [https://a1-3-cyan.vercel.app/](https://a1-3-cyan.vercel.app/)  
📂 **GitHub 저장소**: [https://github.com/woogie0403/A1-3](https://github.com/woogie0403/A1-3)

---


## 목차

- [서비스 소개](#-서비스-소개)
- [주요 기능](#-주요-기능)
- [화면 구성](#-화면-구성)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [AI 기능 명세](#-ai-기능-명세)
- [로컬 실행 방법](#-로컬-실행-방법)
- [Vercel 배포 방법](#-vercel-배포-방법)
- [환경 변수](#-환경-변수)

---

## 🗺️ 서비스 소개

**여기로(Yeogiro)** 는 "어디 갈지 고민"을 AI가 대신 해결해주는 국내 여행 코스 플래너입니다.

여행지·기간·동행자·이동수단·테마를 입력하면 Google Gemini AI가 **하루 4개 스팟(관광 → 맛집 → 카페 → 저녁/야경)** 으로 구성된 동선 최적화 코스를 자동으로 설계합니다.

- 모든 식당·카페는 **직전 스팟에서 10분 이내** 배치 → 동선 낭비 제로
- **1인 기준 예상 경비**(식비+카페+입장료) 함께 제공
- 깔끔하고 직관적인 UI로 설계된 반응형 웹 서비스

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 🤖 AI 코스 생성 | Gemini API로 맞춤 국내 여행 일정 자동 생성 |
| 🗺️ 동선 최적화 | 직전 스팟 반경 10분 이내 맛집·카페 자동 배치 |
| 💰 예상 경비 계산 | 1인 기준 식비·카페·입장료 범위 제공 |
| 📍 테마 카테고리 | 힐링·자연 / 로컬 미식 / 감성 핫플 / 액티비티 / 오션뷰 |
| 🏙️ 퀵 태그 | 제주·강릉·경주·부산·여수·전주 인기 여행지 원클릭 입력 |
| ⚠️ 실패 처리 | 빈 입력 / API 오류 / 타임아웃 안내 메시지 |
| 📋 일정 복사 | 생성된 코스를 클립보드로 한 번에 복사 공유 |
| 📱 반응형 UI | 모바일·태블릿·데스크톱 전 기기 대응 |

---

## 🖥️ 화면 구성

| 섹션 | 설명 |
|------|------|
| **① Hero 섹션** | 시그니처 검색 캡슐, 테마 카테고리 바, 인기 여행지 퀵 태그 |
| **② AI 플래너 섹션** | AI 코스 결과 카드 (타임라인·예산·현지 꿀팁·복사 버튼) |
| **③ 여행 꿀팁 & FAQ 섹션** | 출발 전 필수 체크리스트, 자주 묻는 질문 아코디언 |

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| 프론트엔드 | HTML5, CSS3, Vanilla JavaScript (ES6+) |
| 백엔드 | Vercel Serverless Functions (Python 3.x) |
| AI API | Google Gemini API (`generateContent`) |
| 배포 | Vercel (GitHub 연동 자동 배포) |

> 프레임워크(React/Vue 등) 미사용 — 순수 바닐라 구현

---

## 📁 프로젝트 구조

```
A1-3/
├── index.html          # 메인 페이지 (3개 섹션 전체 포함)
├── css/
│   └── style.css       # 여기로 감성 스타일
├── js/
│   └── app.js          # 폼 처리, fetch 호출, AI 결과 렌더링
├── api/
│   └── generate.py     # Vercel Serverless Function (Gemini API 연동)
├── 기획서.md           # 서비스 기획서
├── requirements.txt    # Python 패키지 의존성
├── .gitignore
└── README.md
```

---

## 🤖 AI 기능 명세

### 입력 파라미터

| 파라미터 | 예시 |
|----------|------|
| 여행지 | 제주도, 강릉, 경주 (국내 한정) |
| 기간 | 당일치기 / 1박 2일 / 2박 3일 |
| 동행자 | 연인·데이트 / 나홀로 / 친구들 / 가족·부모님 |
| 이동수단 | 렌트카/자차 / 뚜벅이/대중교통 |
| 테마 | 힐링·자연 / 로컬 미식 / 감성 핫플 / 액티비티 / 오션뷰 |

### 출력 형식

```json
{
  "title": "제주 서쪽 감성 힐링 코스",
  "summary": "바다 바람과 돌담길을 따라 여유롭게 즐기는 감성 여정",
  "budget": "약 75,000원 ~ 90,000원",
  "timeline": [
    { "time": "오전 10:00", "name": "협재해변", "category": "관광", ... },
    { "time": "오후 12:30", "name": "로컬 맛집",  "category": "맛집", ... },
    { "time": "오후 15:00", "name": "감성 카페",  "category": "카페", ... },
    { "time": "오후 19:00", "name": "야경 명소",  "category": "저녁", ... }
  ],
  "tips": "현지 꿀팁"
}
```

### 실패 처리 시나리오

| 상황 | 안내 메시지 |
|------|------------|
| 빈 입력 | "국내 여행지 이름을 입력해 주세요" |
| 해외 도시 입력 | "국내 전용 서비스입니다" |
| API 오류 (4xx/5xx) | "서버 오류가 발생했습니다" |
| 타임아웃 (30초 초과) | "잠시 후 다시 시도해 주세요" |

---

## 💻 로컬 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/woogie0403/A1-3.git
cd A1-3
```

### 2. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```
GEMINI_API_KEY=여기에_본인의_Gemini_API_키_입력
```

> Google AI Studio(https://aistudio.google.com)에서 무료 발급 가능

### 3. Python 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. Vercel CLI로 로컬 실행

```bash
npm install -g vercel
vercel dev
```

브라우저에서 `http://localhost:3000` 접속

---

## 🚀 Vercel 배포 방법

1. [vercel.com](https://vercel.com)에 GitHub 계정으로 로그인
2. **New Project** → `A1-3` 저장소 선택 → **Import**
3. **Environment Variables** 탭에서 아래 값 추가
4. **Deploy** 클릭

배포 완료 후 발급되는 URL에서 전체 기능 동작을 확인합니다.

---

## 🔐 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `GEMINI_API_KEY` | Google Gemini API 키 | ✅ |

> **보안 주의**: API 키는 절대 코드·README·스크린샷에 직접 노출하지 마세요.  
> `.env` 파일은 `.gitignore`에 포함되어 있으며, Vercel 환경 변수로만 관리합니다.

---

## 🛠️ 트러블슈팅 및 문제 해결 (Troubleshooting)

### 1. Gemini API 일시 부하(503 Service Unavailable) 및 서버 오류 대응
* **문제 상황**: 배포 직후 AI 코스 생성 시 `AI 서버와 통신 중 오류가 발생했습니다 (502/503)` 토스트 발생.
* **원인 분석**: 구글 Gemini 특정 모델(`gemini-3.5-flash`)의 일시적 트래픽 집중으로 인한 서비스 지연 발생.
* **해결 방법**: 즉각 응답 가능한 안정형 모델(`gemini-3.5-flash-lite`)을 1순위로 채택하고, 4개 모델 후보(`gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.8-flash`, `gemini-flash-latest`)에 대해 자동 순차 폴백(Fallback Retry) 로직을 백엔드에 구축하여 99.9% 무중단 응답 보장.

### 2. AI 환각(가짜 맛집 상호명) 억제 및 실존 유명 핫플 보장
* **문제 상황**: 지도 API가 없는 상태에서 존재하지 않는 가상의 식당/카페 이름(예: 제주안성가든 등)이 생성됨.
* **해결 방법**:
  1. `temperature`를 기존 `0.9`에서 `0.2`로 대폭 하향하여 생성형 AI의 과도한 상상력을 억제하고 훈련된 팩트 데이터 추출을 유도.
  2. 네이버 지도, 카카오맵, 블루리본 서베이에 등록된 대표 유명 실존 상호명(예: 부산 초량밀면, 이재모피자 본점, 해운대 암소갈비집 등)만 작성하도록 프롬프트에 엄격한 규칙 부여.

### 3. 다일차(1박 2일, 2박 3일) 일정 미분리 문제 해결
* **문제 상황**: 여행 기간에서 '1박 2일'이나 '2박 3일'을 선택해도 당일치기 코스(4개 스팟)만 생성되던 현상.
* **해결 방법**:
  1. 백엔드에서 `duration` 파라미터에 따라 '당일치기(4개)', '1박 2일(1·2일차 6~8개)', '2박 3일(1·2·3일차 8~10개)'로 동적 프롬프트 분기 처리.
  2. 프론트엔드 UI에 일차(Day)가 바뀔 때마다 `🗓️ 1일차`, `🗓️ 2일차` 구분 배너를 삽입하여 직관적인 시간대별 뷰 완성.

