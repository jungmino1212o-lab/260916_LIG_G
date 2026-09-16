# 🍽️ 오늘 뭐먹지?

**오늘 뭐먹지?**는 지역, 음식 종류, 예산, 인원, 분위기, 추가 요청사항을 입력하면 조건에 맞는 맛집을 추천해주는 Python Flask 기반 웹 애플리케이션입니다.

---

## 🌟 주요 특징

1. **조건 기반 맛집 추천**
   - 지역(직접 입력 + 빠른 선택 칩), 음식 종류, 예산, 인원, 분위기(중복 선택) 입력
   - 자유 텍스트 추가 요청사항(주차, 웨이팅, 예약, 반려동물 동반 등) 키워드 반영
   - 규칙 기반 점수 산정으로 조건에 가장 잘 맞는 맛집을 상위에 노출

2. **맛집 카드 결과**
   - 이름 · 음식 종류 · 지역 · 평점 · 가격대 · 추천 이유
   - 대표 메뉴 / 주소 / 영업시간은 "상세보기" 토글로 확인
   - "지도 보기" 클릭 시 새 탭에서 지도 검색 결과로 이동

3. **프리미엄 글래스모피즘 & 모던 디자인**
   - 다크 모드(기본) 및 라이트 모드 실시간 원클릭 전환
   - 한글 전용 Pretendard 웹폰트와 반응형 레이아웃(모바일 가로 스크롤 없음)

4. **안정적인 오류 처리**
   - 조건 미입력, 추천 결과 없음, 서버 오류 상황별 안내 메시지 제공
   - 내부 traceback/경로 등 민감 정보는 사용자에게 노출하지 않음

> ⚠️ 현재 추천 데이터는 [restaurants.py](restaurants.py)에 포함된 데모용 샘플 데이터입니다. 실서비스 전환 시 외부 맛집 API로 교체하는 것을 전제로 구조가 설계되어 있습니다.

---

## 🚀 빠른 시작 (실행 방법)

### 방법 1. 더블 클릭으로 간편 실행 (가장 쉬운 방법)
- 폴더 내 **`run.bat`** 파일을 더블 클릭하면 자동으로 브라우저가 열리며 앱이 실행됩니다.

### 방법 2. 터미널(명령 프롬프트 / PowerShell)에서 실행
```bash
# 1. 앱 폴더로 이동
cd LIG_DNA_TODO_APP

# 2. 패키지 설치
python -m pip install -r requirements.txt

# 3. 앱 실행
python app.py
```
실행 후 웹 브라우저에서 **`http://127.0.0.1:5000`** 으로 접속합니다.

---

## 📁 프로젝트 구조

```
LIG_DNA_TODO_APP/
├── app.py                 # Flask 메인 서버 및 /api/recommend API
├── restaurants.py          # 맛집 샘플 데이터 및 추천(필터/점수) 로직
├── requirements.txt        # 의존성 패키지 정의
├── run.bat                 # 윈도우 원클릭 자동 실행 배치 스크립트
├── vercel.json              # Vercel 배포 설정 (@vercel/python)
├── test_app.py              # 자동화 테스트 (index, /api/recommend)
├── README.md                # 프로젝트 매뉴얼
├── templates/
│   └── index.html          # 조건 입력 폼 + 결과 카드 SPA 템플릿
└── static/
    ├── css/
    │   └── style.css        # 디자인 시스템 및 테마 스타일시트
    └── js/
        └── app.js            # 조건 수집, /api/recommend 통신, 결과 렌더링
```

---

## 🔌 API

### `POST /api/recommend`
요청 예시:
```json
{
  "location": "강남",
  "food_type": "양식",
  "budget": "2~3만원",
  "people": "2명",
  "mood": ["데이트", "분위기 좋은"],
  "request": "주차 가능한 곳이면 좋겠어요"
}
```
- `location` 또는 `food_type` 중 최소 하나는 필요합니다.
- 응답: `{"status": "success", "results": [...]}` (조건에 맞는 곳이 없으면 `results`는 빈 배열)

---

## ☁️ 배포 (Vercel)

GitHub 저장소를 Vercel 프로젝트에 연결하면 `vercel.json`(@vercel/python 런타임)에 따라 `app.py`가 서버리스 함수로 배포됩니다. 별도의 외부 API 키 없이 현재 샘플 데이터 기반으로 동작합니다.
