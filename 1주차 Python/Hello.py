# Flask import
from flask import Flask

# Flask 앱을 생성
app = Flask(__name__)

# 편의를 위해 디버그 모드를 활성화
app.debug = True

# URL 경로에 따라 실행할 함수에 데코레이터 사용 (경로)
@app.route("/")
# 앞 경로에 접근하면 실행할 함수를 지정
def hello():
    return "Hello World"

# <name>자리에 오는 문자열은 name에 할당되어 함수로 전달
@app.route("/hello/<name>")
def hello_to(name):
    return "Hello, {}!".format(name)

# 이 파일을 바로 실행할 때 함께 실행할 코드를 작성
if __name__ == "__main__":
    app.run()
