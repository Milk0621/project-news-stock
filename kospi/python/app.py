from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # CORS 설정은 app 생성 후 바로 적용

@app.route('/api/keys')
def get_keys():
    return jsonify({
        'appkey': os.getenv("appkey"),
        'secretkey': os.getenv("secretkey")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

