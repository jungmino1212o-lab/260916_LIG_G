import unittest
import json
from app import app


class TestFoodFinderApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_01_index_route(self):
        """메인 페이지 HTML 서빙 확인"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('오늘 뭐먹지', response.get_data(as_text=True))

    def test_02_recommend_success(self):
        """정상적인 조건으로 맛집 추천 요청"""
        payload = {
            "location": "강남",
            "food_type": "양식",
            "budget": "2~3만원",
            "people": 2,
            "mood": ["데이트"],
            "request": "주차 가능한 곳이면 좋겠어요"
        }
        res = self.client.post('/api/recommend', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['results'], list)
        self.assertGreater(len(data['results']), 0)
        first = data['results'][0]
        for field in ('name', 'food_type', 'region', 'price_display', 'reason', 'map_query'):
            self.assertIn(field, first)

    def test_03_recommend_missing_conditions(self):
        """지역/음식 종류가 모두 없으면 오류 반환"""
        res = self.client.post('/api/recommend', json={})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'error')

    def test_04_recommend_no_match(self):
        """조건에 맞는 결과가 없을 때 빈 목록 반환"""
        payload = {"location": "부산", "food_type": "상관없음"}
        res = self.client.post('/api/recommend', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['results'], [])


if __name__ == '__main__':
    unittest.main()
