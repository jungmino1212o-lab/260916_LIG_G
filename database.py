import sqlite3
import os
from datetime import datetime

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/todo.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "todo.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT DEFAULT '업무',
            priority TEXT DEFAULT '보통',
            due_date TEXT DEFAULT '',
            completed INTEGER DEFAULT 0,
            is_starred INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT DEFAULT ''
        )
    """)
    conn.commit()

    # 테이블이 비어있으면 초기 샘플 데이터 입력
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_tasks = [
            (
                "LIG DNA 혁신 과제 현황 점검",
                "팀별 디지털 전환(DX) 및 RPA 자동화 프로세스 적용 지표 분석 보고서 작성",
                "DNA혁신",
                "긴급",
                datetime.now().strftime("%Y-%m-%d"),
                0,
                1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ""
            ),
            (
                "업무 자동화 RPA 봇 스케줄링 검증",
                "주간 배치 작업 자동화 스크립트 실행 로그 점검 및 예외 알림 채널 연동 확인",
                "업무",
                "높음",
                datetime.now().strftime("%Y-%m-%d"),
                0,
                1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ""
            ),
            (
                "차세대 프로젝트 아키텍처 리뷰 회의",
                "클라우드 인프라 확장 및 MSA 연계 방안 논의 (대회의실 14:00)",
                "프로젝트",
                "보통",
                "",
                1,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "생성형 AI 프롬프트 엔지니어링 스터디",
                "Claude 및 GPT-4o 기반 사내 워크플로우 최적화 베스트 프랙티스 정리",
                "학습",
                "낮음",
                "",
                0,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ""
            )
        ]
        cursor.executemany("""
            INSERT INTO todos (title, description, category, priority, due_date, completed, is_starred, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_tasks)
        conn.commit()

    conn.close()

def get_all_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY is_starred DESC, completed ASC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_todo(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO todos (title, description, category, priority, due_date, completed, is_starred, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?, 0, ?, ?, '')
    """, (
        data.get("title", "").strip(),
        data.get("description", "").strip(),
        data.get("category", "업무"),
        data.get("priority", "보통"),
        data.get("due_date", ""),
        1 if data.get("is_starred") else 0,
        created_at
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_todo(todo_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE todos 
        SET title = ?, description = ?, category = ?, priority = ?, due_date = ?
        WHERE id = ?
    """, (
        data.get("title", "").strip(),
        data.get("description", "").strip(),
        data.get("category", "업무"),
        data.get("priority", "보통"),
        data.get("due_date", ""),
        todo_id
    ))
    conn.commit()
    conn.close()

def toggle_complete(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row:
        new_state = 0 if row["completed"] else 1
        comp_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_state == 1 else ""
        cursor.execute("UPDATE todos SET completed = ?, completed_at = ? WHERE id = ?", (new_state, comp_time, todo_id))
        conn.commit()
    conn.close()
    return new_state if row else None

def toggle_star(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_starred FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row:
        new_state = 0 if row["is_starred"] else 1
        cursor.execute("UPDATE todos SET is_starred = ? WHERE id = ?", (new_state, todo_id))
        conn.commit()
    conn.close()
    return new_state if row else None

def delete_todo(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

def clear_completed_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE completed = 1")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM todos")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
    completed = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM todos WHERE is_starred = 1 AND completed = 0")
    starred = cursor.fetchone()[0]
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM todos WHERE due_date = ? AND completed = 0", (today_str,))
    due_today = cursor.fetchone()[0]
    
    conn.close()
    
    progress = round((completed / total * 100)) if total > 0 else 0
    return {
        "total": total,
        "completed": completed,
        "active": total - completed,
        "starred": starred,
        "due_today": due_today,
        "progress": progress
    }
