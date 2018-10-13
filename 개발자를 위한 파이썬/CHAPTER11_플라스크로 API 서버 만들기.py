'''
CHAPTER11 플라스크로 API 서버 만들기¶
- 설치와 Hello World 웹 페이지 실행하기
- 파라미터로 URL 경로와 쿼리 추가하기
- API 서버 만들기
'''


# 11.1 설치와 Hello World 웹페이지 실행하기
# Flask import
from flask import Flask, request
import sqlite3
import json

# Flask 앱을 생성합니다.
app = Flask(__name__)

'''
# URL 경로에 따라 실행할 함수에 데코레이터 사용합니다. (경로)
@app.route("/")
# 앞 경로에 접근하면 실행할 함수를 지정합니다.
def hello():
    return "Hello World"
# http://localhost:5000 경로로 접속합니다.


# 11.2 파라미터로 URL 경로와 쿼리 추가하기

@app.route("/hello/<name>")
def hello_to(name):
    return "Hello {}!".format(name)

# http://localhost:5000/hello/JI 경로로 접속합니다.
'''

# 11.3 API 서버 만들기
# API는 Application Program Interface의 약자입니다.
# 의미는 서로 다른 프로그램 사이에 통신할 수 있는 약속이라 할 수 있습니다.


# 11.3.1 데이터베이스와 연결하기

def get_db_con() -> sqlite3.connect:
    return sqlite3.connect("db.sqlite")

# 11.3.2 모든 데이터 내려받기
# URL 경로에 따라 실행할 함수에 데코레이터를 사용합니다. 데코레이터의 파라미터는 URL 경로입니다.
@app.route("/")
# 모든 데이터를 내려받기 위한 hello() 함수를 정의합니다.
def hello():
    # con이라는 변수를 생성해 데이터베이스에 연결합니다.
    with get_db_con() as con:
        cur = con.cursor()

        # hanbit_books 데이터베이스의 모든 데이터를 선택합니다.
        q = "SELECT * FROM hanbit_books"
        result = cur.execute(q)

    # 결과를 json 문자열로 만들어줍니다.
    result_json = jsonize(result)

    # 결과를 돌려줍니다.
    return result_json

# 11.3.3 조건에 따라 데이터 가져오기
# 저자 이름으로 요청받을 URL을 설정합니다.
@app.route("/books/by/author")
def get_books_by_author():
    # 파라미터에서 name을 받아옵니다.
    name = request.args.get("name")

    # 데이터베이스 연결을 가져와서 작업합니다.
    # 작업이 끝나면 자동으로 with close를 호출합니다.
    with get_db_con() as con:
        # 커서를 가져옵니다.
        cur = con.cursor()

        # hanbit_books 테이블에서 author 열이 name과 일치하는 것을 찾아옵니다.
        q = "SELECT * FROM hanbit_books WHERE author LIKE :name ORDER BY title"
        param = { "name" : "%" + name + "%" }
        result = cur.execute(q, param)

    # 결과를 JSON 문자열로 만들어줍니다.
    result_json = jsonize(result)

    # 결과를 돌려줍니다.
    return result_json


# 출간월을 요청받을 URL을 설정합니다.
@app.route("/books/by/month")
def get_books_by_month():
    # 파라미터에서 name을 받아옵니다.
    month = request.args.get("month")

    # 숫자가 한 자리일 경우 앞에 "0"을 붙입니다.
    if int(month) < 10:
        month = "0" + month

    # 데이터베이스 연결을 가져와서 작업합니다.
    # 작업이 끝나면 자동으로 with close를 호출합니다.
    with get_db_con() as con:
        # 커서를 가져옵니다.
        cur = con.cursor()

        # 쿼리를 작성합니다. 월 부분이 month와 일치하는 걸 찾아옵니다.
        q = "SELECT * FROM hanbit_books WHERE strftime('%m', pub_date) = :month ORDER BY pub_date DESC"
        param = { "month" : month }
        result = cur.execute(q, param)

    # 결과를 JSON 문자열로 만들어줍니다.
    result_json = jsonize(result)

    # 결과를 돌려줍니다.
    return result_json


# 데이터베이스 커서의 result를 전달받아서 JSON 문자열로 만드는 함수입니다.
def jsonize(result):
    result_json = json.dumps(list(result.fetchall()), ensure_ascii = False).encode("UTF-8")
    return result_json


# 이 파일을 바로 실행할 때 함께 실행할 코드를 작성합니다.
if __name__ == "__main__":
    app.run(debug = True)
