from flask import Flask, render_template, request, jsonify, Response
import json
import database as db

app = Flask(__name__)

# 데이터베이스 초기화
db.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = db.get_all_todos()
    return jsonify({"status": "success", "todos": todos})

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or not data.get('title', '').strip():
        return jsonify({"status": "error", "message": "할 일 제목을 입력해주세요."}), 400
    
    new_id = db.add_todo(data)
    return jsonify({"status": "success", "id": new_id, "message": "성공적으로 추가되었습니다."}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data or not data.get('title', '').strip():
        return jsonify({"status": "error", "message": "할 일 제목을 입력해주세요."}), 400
    
    db.update_todo(todo_id, data)
    return jsonify({"status": "success", "message": "성공적으로 수정되었습니다."})

@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle_todo(todo_id):
    new_state = db.toggle_complete(todo_id)
    if new_state is None:
        return jsonify({"status": "error", "message": "항목을 찾을 수 없습니다."}), 404
    return jsonify({"status": "success", "completed": bool(new_state)})

@app.route('/api/todos/<int:todo_id>/star', methods=['POST'])
def toggle_star(todo_id):
    new_state = db.toggle_star(todo_id)
    if new_state is None:
        return jsonify({"status": "error", "message": "항목을 찾을 수 없습니다."}), 404
    return jsonify({"status": "success", "is_starred": bool(new_state)})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    db.delete_todo(todo_id)
    return jsonify({"status": "success", "message": "삭제되었습니다."})

@app.route('/api/todos/clear-completed', methods=['POST'])
def clear_completed():
    count = db.clear_completed_todos()
    return jsonify({"status": "success", "deleted_count": count})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = db.get_stats()
    return jsonify({"status": "success", "stats": stats})

@app.route('/api/export', methods=['GET'])
def export_data():
    todos = db.get_all_todos()
    data_str = json.dumps(todos, ensure_ascii=False, indent=2)
    return Response(
        data_str,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=lig_dna_todos_backup.json"}
    )

if __name__ == '__main__':
    print("==================================================")
    print("   LIG DNA TODO APP 서버가 시작되었습니다.")
    print("   접속 주소: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
