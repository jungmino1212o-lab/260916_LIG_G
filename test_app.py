import unittest
import json
import os
from app import app
import database as db

class TestLigDnaTodoApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_01_index_route(self):
        """메인 페이지 HTML 서빙 확인"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('LIG DNA', response.get_data(as_text=True))

    def test_02_get_todos(self):
        """할 일 목록 조회 API 확인"""
        response = self.client.get('/api/todos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['todos'], list)

    def test_03_add_todo_and_crud(self):
        """할 일 추가, 수정, 완료 토글, 중요 토글, 삭제 전체 사이클 확인"""
        # 1. 등록
        payload = {
            "title": "테스트 업무 단위 시험",
            "category": "업무",
            "priority": "긴급",
            "due_date": "2026-09-30",
            "is_starred": True,
            "description": "자동화 테스트 실행 중"
        }
        res = self.client.post('/api/todos', json=payload)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')
        new_id = data['id']

        # 2. 수정
        update_payload = {
            "title": "테스트 업무 수정됨",
            "category": "DNA혁신",
            "priority": "높음",
            "due_date": "2026-10-01",
            "description": "설명 내용 수정됨"
        }
        update_res = self.client.put(f'/api/todos/{new_id}', json=update_payload)
        self.assertEqual(update_res.status_code, 200)

        # 3. 완료 토글
        toggle_res = self.client.post(f'/api/todos/{new_id}/toggle')
        self.assertEqual(toggle_res.status_code, 200)
        toggle_data = json.loads(toggle_res.data)
        self.assertTrue(toggle_data['completed'])

        # 4. 중요(Star) 토글
        star_res = self.client.post(f'/api/todos/{new_id}/star')
        self.assertEqual(star_res.status_code, 200)

        # 5. 삭제
        del_res = self.client.delete(f'/api/todos/{new_id}')
        self.assertEqual(del_res.status_code, 200)

    def test_04_stats(self):
        """통계 API 확인"""
        res = self.client.get('/api/stats')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('total', data['stats'])
        self.assertIn('progress', data['stats'])

    def test_05_export(self):
        """데이터 백업 API 확인"""
        res = self.client.get('/api/export')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get('Content-Type'), 'application/json')

if __name__ == '__main__':
    unittest.main()
