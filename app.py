from flask import Flask, render_template, request, jsonify
import restaurants
import places

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json(silent=True) or {}

    location = (data.get('location') or '').strip()
    food_type = (data.get('food_type') or '').strip()

    if not location and not food_type:
        return jsonify({
            "status": "error",
            "message": "지역 또는 원하는 음식 종류를 입력해주세요."
        }), 400

    try:
        if places.is_configured():
            results = places.search(data)
        else:
            results = restaurants.recommend(data)
    except Exception:
        app.logger.exception("맛집 추천 처리 중 오류가 발생했습니다.")
        return jsonify({
            "status": "error",
            "message": "추천을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."
        }), 500

    return jsonify({
        "status": "success",
        "results": results,
        "source": "kakao" if places.is_configured() else "sample"
    })


if __name__ == '__main__':
    print("==================================================")
    print("   오늘 뭐먹지? 서버가 시작되었습니다.")
    print("   접속 주소: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
