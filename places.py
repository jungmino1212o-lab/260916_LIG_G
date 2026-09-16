"""카카오 로컬(키워드 검색) API를 이용한 실제 맛집 검색.

Kakao Local API는 평점/리뷰수/가격대/영업시간/대표메뉴를 제공하지 않는다.
해당 필드는 None으로 반환하며, 프론트엔드에서 "정보 없음" 처리하거나 화면에서 뺀다.
API Key(KAKAO_REST_API_KEY)가 설정되지 않은 경우 is_configured()가 False를 반환하여
호출 측(app.py)이 로컬 샘플 데이터(restaurants.py)로 대체할 수 있도록 한다.
"""

import os
import requests

KAKAO_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
KAKAO_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

CAFE_DESSERT_TYPES = {"카페", "디저트"}


def is_configured():
    return bool(KAKAO_API_KEY)


def _build_query(criteria):
    location = (criteria.get("location") or "").strip()
    food_type = (criteria.get("food_type") or "").strip()
    parts = []
    if location:
        parts.append(location)
    if food_type and food_type != "상관없음":
        parts.append(food_type)
    parts.append("맛집")
    return " ".join(parts)


def search(criteria, limit=6):
    if not KAKAO_API_KEY:
        raise RuntimeError("KAKAO_REST_API_KEY가 설정되지 않았습니다.")

    food_type = (criteria.get("food_type") or "").strip()
    query = _build_query(criteria)

    params = {"query": query, "size": min(max(limit, 1), 15)}
    if food_type in CAFE_DESSERT_TYPES:
        params["category_group_code"] = "CE7"
    elif food_type and food_type != "상관없음":
        params["category_group_code"] = "FD6"

    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    resp = requests.get(KAKAO_SEARCH_URL, headers=headers, params=params, timeout=6)
    resp.raise_for_status()
    documents = resp.json().get("documents", [])

    results = []
    for doc in documents[:limit]:
        category_parts = [c.strip() for c in (doc.get("category_name") or "").split(">") if c.strip()]
        cuisine = category_parts[-1] if category_parts else None

        results.append({
            "name": doc.get("place_name"),
            "cuisine": cuisine,
            "region": (criteria.get("location") or "").strip() or None,
            "address": doc.get("road_address_name") or doc.get("address_name") or None,
            "phone": doc.get("phone") or None,
            "map_url": doc.get("place_url") or None,
            "rating": None,
            "review_count": None,
            "price_display": None,
            "hours": None,
            "signature_menu": None,
            "reason": f"'{query}' 검색 결과로 찾은 실제 매장입니다. 평점·가격·분위기 등 상세 정보는 지도에서 확인해주세요.",
        })
    return results
