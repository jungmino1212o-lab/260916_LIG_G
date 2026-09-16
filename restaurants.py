"""맛집 추천 데이터 및 추천 로직.

RESTAURANTS는 데모/샘플 큐레이션 데이터이며 실제 영업 정보와 다를 수 있다.
실서비스 전환 시 외부 맛집 API로 교체하는 것을 전제로 구조를 설계했다.
"""

BUDGET_TIERS = ["1만원 이하", "1~2만원", "2~3만원", "3~5만원", "5만원 이상"]

RESTAURANTS = [
    {
        "name": "역삼 파스타 공방",
        "region": "강남", "region_aliases": ["강남", "강남구", "역삼", "서울"],
        "food_type": "양식", "cuisine": "이탈리안",
        "signature_menu": "트러플 크림 파스타",
        "price_tier": "2~3만원", "avg_price_display": "1인 약 27,000원",
        "moods": ["데이트", "분위기 좋은", "조용한"],
        "features": ["주차가능", "웨이팅짧음", "예약가능"],
        "rating": 4.6, "review_count": 482,
        "hours": "매일 11:30 - 22:00 (라스트오더 21:00)",
        "address": "서울 강남구 역삼동 일대",
        "description": "아늑한 조명과 잔잔한 음악이 흐르는 파스타 전문점.",
    },
    {
        "name": "강남 스테이크 하우스",
        "region": "강남", "region_aliases": ["강남", "강남구", "서울"],
        "food_type": "양식", "cuisine": "스테이크",
        "signature_menu": "안심 스테이크 세트",
        "price_tier": "3~5만원", "avg_price_display": "1인 약 38,000원",
        "moods": ["데이트", "회식", "분위기 좋은"],
        "features": ["주차가능", "단체가능", "룸있음"],
        "rating": 4.5, "review_count": 356,
        "hours": "매일 12:00 - 22:30",
        "address": "서울 강남구 논현동 일대",
        "description": "묵직한 인테리어와 넓은 좌석으로 회식에도 좋은 곳.",
    },
    {
        "name": "강남 한우 명가",
        "region": "강남", "region_aliases": ["강남", "강남구", "서울"],
        "food_type": "고기", "cuisine": "한우",
        "signature_menu": "한우 모듬 특수부위",
        "price_tier": "5만원 이상", "avg_price_display": "1인 약 55,000원",
        "moods": ["회식", "가족", "분위기 좋은"],
        "features": ["주차가능", "단체가능", "룸있음"],
        "rating": 4.7, "review_count": 610,
        "hours": "매일 11:30 - 22:00",
        "address": "서울 강남구 대치동 일대",
        "description": "품질 좋은 한우와 넉넉한 룸 좌석으로 회식에 적합.",
    },
    {
        "name": "강남 이자카야 소라",
        "region": "강남", "region_aliases": ["강남", "강남구", "서울"],
        "food_type": "일식", "cuisine": "이자카야",
        "signature_menu": "모듬 사시미와 사케",
        "price_tier": "2~3만원", "avg_price_display": "1인 약 26,000원",
        "moods": ["캐주얼", "회식", "혼밥"],
        "features": ["웨이팅짧음", "예약가능"],
        "rating": 4.4, "review_count": 298,
        "hours": "매일 17:00 - 01:00",
        "address": "서울 강남구 신사동 일대",
        "description": "퇴근 후 가볍게 들르기 좋은 이자카야.",
    },
    {
        "name": "강남 국밥 한그릇",
        "region": "강남", "region_aliases": ["강남", "강남구", "서울"],
        "food_type": "한식", "cuisine": "국밥",
        "signature_menu": "순댓국",
        "price_tier": "1만원 이하", "avg_price_display": "1인 약 9,000원",
        "moods": ["혼밥", "캐주얼"],
        "features": ["웨이팅짧음"],
        "rating": 4.3, "review_count": 512,
        "hours": "매일 24시간",
        "address": "서울 강남구 역삼동 일대",
        "description": "혼자서도 부담 없이 빠르게 먹기 좋은 국밥집.",
    },
    {
        "name": "홍대 화덕피자집",
        "region": "홍대", "region_aliases": ["홍대", "홍대입구", "마포", "서울"],
        "food_type": "양식", "cuisine": "이탈리안",
        "signature_menu": "마르게리타 화덕피자",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 18,000원",
        "moods": ["캐주얼", "데이트", "분위기 좋은"],
        "features": ["웨이팅짧음"],
        "rating": 4.5, "review_count": 421,
        "hours": "매일 12:00 - 23:00",
        "address": "서울 마포구 서교동 일대",
        "description": "화덕에서 바로 구워내는 얇은 피자가 인기인 캐주얼 다이닝.",
    },
    {
        "name": "홍대 마라탕 공작소",
        "region": "홍대", "region_aliases": ["홍대", "마포", "서울"],
        "food_type": "중식", "cuisine": "마라탕",
        "signature_menu": "마라샹궈",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 15,000원",
        "moods": ["캐주얼", "혼밥"],
        "features": ["웨이팅짧음", "단체가능"],
        "rating": 4.2, "review_count": 389,
        "hours": "매일 11:00 - 23:00",
        "address": "서울 마포구 동교동 일대",
        "description": "매운맛 단계를 직접 고를 수 있는 캐주얼 중식당.",
    },
    {
        "name": "홍대 감성 브런치",
        "region": "홍대", "region_aliases": ["홍대", "마포", "서울"],
        "food_type": "카페", "cuisine": "브런치카페",
        "signature_menu": "에그 베네딕트",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 17,000원",
        "moods": ["데이트", "분위기 좋은", "조용한"],
        "features": ["웨이팅짧음", "반려동물동반"],
        "rating": 4.6, "review_count": 275,
        "hours": "매일 09:00 - 20:00",
        "address": "서울 마포구 연남동 일대",
        "description": "햇살 좋은 창가 자리가 인기인 아기자기한 브런치 카페.",
    },
    {
        "name": "홍대 치킨앤크래프트",
        "region": "홍대", "region_aliases": ["홍대", "마포", "서울"],
        "food_type": "치킨", "cuisine": "치킨·맥주",
        "signature_menu": "크래프트 반반치킨",
        "price_tier": "2~3만원", "avg_price_display": "1인 약 22,000원",
        "moods": ["캐주얼", "회식"],
        "features": ["단체가능", "웨이팅짧음"],
        "rating": 4.4, "review_count": 344,
        "hours": "매일 16:00 - 02:00",
        "address": "서울 마포구 서교동 일대",
        "description": "다양한 크래프트 맥주와 함께 즐기는 치킨집.",
    },
    {
        "name": "성수 오마카세 온",
        "region": "성수", "region_aliases": ["성수", "성수동", "성동구", "서울"],
        "food_type": "일식", "cuisine": "오마카세",
        "signature_menu": "런치 오마카세 12피스",
        "price_tier": "5만원 이상", "avg_price_display": "1인 약 80,000원",
        "moods": ["데이트", "분위기 좋은", "조용한"],
        "features": ["예약가능", "룸있음"],
        "rating": 4.8, "review_count": 210,
        "hours": "화-일 12:00 - 21:30 (월요일 휴무)",
        "address": "서울 성동구 성수동 일대",
        "description": "셰프가 직접 설명해주는 프리미엄 오마카세.",
    },
    {
        "name": "성수 감성 로스터리",
        "region": "성수", "region_aliases": ["성수", "성동구", "서울"],
        "food_type": "카페", "cuisine": "스페셜티커피",
        "signature_menu": "핸드드립 세트",
        "price_tier": "1만원 이하", "avg_price_display": "1인 약 8,000원",
        "moods": ["조용한", "혼밥", "분위기 좋은"],
        "features": ["웨이팅짧음", "반려동물동반"],
        "rating": 4.5, "review_count": 389,
        "hours": "매일 10:00 - 21:00",
        "address": "서울 성동구 성수동 일대",
        "description": "공장을 개조한 넓은 공간에서 즐기는 스페셜티 커피.",
    },
    {
        "name": "성수 삼겹살 골목",
        "region": "성수", "region_aliases": ["성수", "성동구", "서울"],
        "food_type": "고기", "cuisine": "삼겹살",
        "signature_menu": "숙성 삼겹살",
        "price_tier": "2~3만원", "avg_price_display": "1인 약 24,000원",
        "moods": ["회식", "캐주얼", "가족"],
        "features": ["단체가능", "주차가능"],
        "rating": 4.3, "review_count": 302,
        "hours": "매일 16:00 - 24:00",
        "address": "서울 성동구 성수동 일대",
        "description": "직원이 직접 구워주는 편안한 삼겹살집.",
    },
    {
        "name": "잠실 롯데뷰 다이닝",
        "region": "잠실", "region_aliases": ["잠실", "송파구", "서울"],
        "food_type": "양식", "cuisine": "퓨전다이닝",
        "signature_menu": "안심 스테이크 파스타 세트",
        "price_tier": "3~5만원", "avg_price_display": "1인 약 42,000원",
        "moods": ["데이트", "분위기 좋은"],
        "features": ["뷰맛집", "예약가능"],
        "rating": 4.6, "review_count": 267,
        "hours": "매일 11:00 - 22:00",
        "address": "서울 송파구 잠실동 일대",
        "description": "탁 트인 전망과 함께 즐기는 퓨전 다이닝.",
    },
    {
        "name": "잠실 가족 한정식",
        "region": "잠실", "region_aliases": ["잠실", "송파구", "서울"],
        "food_type": "한식", "cuisine": "한정식",
        "signature_menu": "모듬 한정식 코스",
        "price_tier": "3~5만원", "avg_price_display": "1인 약 33,000원",
        "moods": ["가족", "조용한", "회식"],
        "features": ["주차가능", "단체가능", "룸있음"],
        "rating": 4.5, "review_count": 198,
        "hours": "매일 11:00 - 21:30",
        "address": "서울 송파구 잠실동 일대",
        "description": "정갈한 반찬과 넉넉한 좌석으로 가족 모임에 좋은 곳.",
    },
    {
        "name": "잠실 디저트 라운지",
        "region": "잠실", "region_aliases": ["잠실", "송파구", "서울"],
        "food_type": "디저트", "cuisine": "케이크·티",
        "signature_menu": "시그니처 티라미수",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 14,000원",
        "moods": ["데이트", "조용한", "분위기 좋은"],
        "features": ["웨이팅짧음"],
        "rating": 4.4, "review_count": 176,
        "hours": "매일 10:30 - 21:00",
        "address": "서울 송파구 신천동 일대",
        "description": "조용히 대화하기 좋은 아늑한 디저트 카페.",
    },
    {
        "name": "서울 중식당 금룡",
        "region": "서울", "region_aliases": ["서울", "종로", "중구"],
        "food_type": "중식", "cuisine": "정통중식",
        "signature_menu": "탕수육과 짬뽕",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 16,000원",
        "moods": ["가족", "캐주얼", "회식"],
        "features": ["단체가능", "주차가능"],
        "rating": 4.3, "review_count": 233,
        "hours": "매일 11:00 - 21:30",
        "address": "서울 종로구 일대",
        "description": "오랜 전통의 정통 중식 코스 요리 전문점.",
    },
    {
        "name": "서울 혼밥 초밥",
        "region": "서울", "region_aliases": ["서울", "종로", "중구"],
        "food_type": "일식", "cuisine": "회전초밥",
        "signature_menu": "모듬 초밥 세트",
        "price_tier": "1~2만원", "avg_price_display": "1인 약 19,000원",
        "moods": ["혼밥", "캐주얼"],
        "features": ["웨이팅짧음"],
        "rating": 4.2, "review_count": 154,
        "hours": "매일 11:00 - 22:00",
        "address": "서울 중구 일대",
        "description": "1인 좌석이 잘 갖춰진 부담 없는 초밥집.",
    },
]


def _match_request_keywords(request_text, features):
    keyword_map = {
        "주차": "주차가능",
        "웨이팅": "웨이팅짧음",
        "예약": "예약가능",
        "단체": "단체가능",
        "룸": "룸있음",
        "반려동물": "반려동물동반",
        "강아지": "반려동물동반",
        "뷰": "뷰맛집",
        "전망": "뷰맛집",
    }
    matched = []
    for keyword, feature in keyword_map.items():
        if keyword in request_text and feature in features and feature not in matched:
            matched.append(feature)
    return matched


def _build_reason(restaurant, reason_fragments):
    if reason_fragments:
        return " ".join(reason_fragments[:3]) + f" {restaurant['description']}"
    return restaurant["description"]


def recommend(criteria, limit=6):
    """사용자 조건에 맞춰 RESTAURANTS를 점수화하여 상위 결과를 반환한다."""
    location = (criteria.get("location") or "").strip()
    food_type = (criteria.get("food_type") or "").strip()
    budget = (criteria.get("budget") or "").strip()
    people = str(criteria.get("people") or "").strip()
    moods = criteria.get("mood") or []
    if isinstance(moods, str):
        moods = [m.strip() for m in moods.split(",") if m.strip()]
    request_text = (criteria.get("request") or "").strip()

    # 지역/음식 종류는 하드 필터: 조건을 지정했는데 맞는 곳이 없으면 빈 결과를 반환한다.
    candidates = []
    for r in RESTAURANTS:
        if location and not any(location in alias or alias in location for alias in r["region_aliases"]):
            continue
        if food_type and food_type != "상관없음" and food_type != r["food_type"]:
            continue
        candidates.append(r)

    scored = []
    for r in candidates:
        score = 1
        reasons = []

        if location:
            reasons.append(f"{r['region']} 지역 조건에 맞아요.")

        if food_type and food_type != "상관없음":
            reasons.append(f"찾으시는 {food_type} 메뉴가 있어요.")

        if budget and budget != "상관없음" and budget in BUDGET_TIERS and r["price_tier"] in BUDGET_TIERS:
            diff = abs(BUDGET_TIERS.index(budget) - BUDGET_TIERS.index(r["price_tier"]))
            if diff == 0:
                score += 2
                reasons.append("예산 조건에 맞는 가격대예요.")
            elif diff == 1:
                score += 1

        if moods:
            overlap = [m for m in moods if m in r["moods"]]
            if overlap:
                score += len(overlap) * 2
                reasons.append(f"{'·'.join(overlap)} 분위기를 원하신다면 좋아요.")

        if people:
            if people in ("4명", "5명 이상") and ("단체가능" in r["features"] or "회식" in r["moods"]):
                score += 1
            if people == "1명" and "혼밥" in r["moods"]:
                score += 1

        if request_text:
            matched_features = _match_request_keywords(request_text, r["features"])
            if matched_features:
                score += len(matched_features) * 2
                reasons.append(f"요청하신 조건({', '.join(matched_features)})도 반영했어요.")
            if r["cuisine"] and r["cuisine"] in request_text:
                score += 2
                reasons.append(f"{r['cuisine']} 스타일을 찾으신다면 잘 맞아요.")

        scored.append((score, r, reasons))

    scored.sort(key=lambda item: (-item[0], -item[1]["rating"]))

    results = []
    for score, r, reasons in scored[:limit]:
        results.append({
            "name": r["name"],
            "food_type": r["food_type"],
            "cuisine": r["cuisine"],
            "region": r["region"],
            "signature_menu": r["signature_menu"],
            "price_display": r["avg_price_display"],
            "rating": r["rating"],
            "review_count": r["review_count"],
            "hours": r["hours"],
            "address": r["address"],
            "reason": _build_reason(r, reasons),
            "map_query": f"{r['name']} {r['address']}",
        })
    return results
