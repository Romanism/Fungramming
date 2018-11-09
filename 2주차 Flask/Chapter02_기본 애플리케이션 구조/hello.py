'''
Chapter02 기본 애플리케이션 구조
'''

'''
2.1 초기화
- 모든 플라스크 애플리케이션은 애플리케이션 인스터스를 생성해야 합니다.
- 애플리케이션 인스턴스는 Flask 클래스의 오브젝트입니다.
'''

from flask import Flask

# 플라스크 클래스 생성자에 필요한 한가지 인수는 메인 모듈의 이름이나 애플리케이션의 패키지 이름입니다.
# 대부분의 애플리케이션에서는 파이썬의 __name__변수가 적절한 값입니다.
app = Flask(__name__)


'''
2.2 라우트와 뷰함수
- 라우트(route)는 URL과 이 URL을 처리하는 함수의 관련성을 의미합니다.
- 플라스크에서 라우트를 정의하는 가장 간단한 방법은 @app.route 데코레이터를 사용하는 것입니다.
- route뒤에 괄호에는 경로를 설정해줍니다.
'''

@app.route("/")
def main():
    # 웹 브라우저에 들어가면 서버에서 main()이 트리거되어 실행되는데 이러한 함수를 뷰 함수(View Function)라고 합니다.
    return "<h1>Hello World!<h1>"
    # 파일 실행 후 http://127.0.0.1:5000/ 로 접속

# 동적 함수를 이용해보겠습니다. 동적이라는 것은 상황마다 바뀔수 있다는 것을 의미합니다.
# 플라스크에서 동적 함수를 사용하기 위해선 <>를 통해 변수를 넣고 함수 인자에 해당 변수를 넣어 실행하면 됩니다.
@app.route('/user/<name>/')# user주소에 name이라는 동적 변수를 넣었습니다.
def user(name): # 위의 name을 인자로 받았습니다.
    return "<h1>Hello, %s</h1>" % name
    # 파일 실행 후 http://127.0.0.1:5000/user/JI 로 접속


'''
2.3 서버 시작 (Server Startup)
__name__ == "__main__"는 파이썬 코드가 직접 실행될 때만 개발 웹 서버가 실행된다는 것을 의미합니다. (Ctrl + C로 중지)
if __name__ == "__main__":
    # debug = True를 통해 디버그가 발생시 확인할 수 있습니다. (플라스크만의 장점)
    app.run(debug = True)
'''


'''
2.4 리퀘스트 - 응답 사이클
- 뷰 함수가 필요하지도 않은 너무 많은 인수를 갖는 것을 피하기 위해 플라스크는 컨텍스트(context)를 사용합니다.
- 이를 통해 임시적으로 오브젝트를 글로벌하게 엑세스 할도록 합니다.
- 플라스크에선 두가지 컨텍스트가 있는데 애플리케이션 컨텍스트와 리퀘스트 컨텍스트가 있습니다.
'''

from flask import request
@app.route("/index/")
def index():
    user_agent = request.headers.get("user_Agent")
    return '<p>Your browser is %s </p>' % user_agent


'''
2.5 리퀘스트 디스패치 (보내다)
- 플라스크는 각 라우트에 대한 메소드를 부착(attach)합니다.
- 따라서 같은 URL에 전송된 서로 다른 리퀘스트 메소드라고 하더라도 다른 뷰 함수에 의해 처리됩니다.
'''


'''
2.6 리퀘스트 후크 (걸다)
- 공통 함수를 등록하고 리퀘스트가 뷰 함수에 디스패치되는 전후에 실행되도록 하는 것을 의미합니다.
- 리퀘스트 후크는 데코레이터를 사용해 구현합니다.

- 종류:
1. before_first_request : 함수를 등록해 첫 번째 리퀘스트가 처리되기 전에 실행합니다.
2. before_request : 각 리퀘스트 전에 실행하는 함수를 등록합니다.
3. after_request : 처리되지 않는 예외가 발생하지 않는다면, 각 리퀘스트 이후에 실행하는 함수를 등록합니다.
4. teardown_request : 처리되지 않는 예외가 발생하더라도, 각 리퀘스트 이후에 실행하는 함수를 등록합니다.
'''


'''
2.7 응답 (response)
- 플라스크가 뷰 함수를 호출할 때 리퀘스트에 대한 응답(respose)으로 값을 리턴하게 됩니다.
- 대부분의 경우 응답은 간단한 문자열이며 HTML 페이지로 클라이언트에 전송됩니다.
- HTML 응답의 가장 중요한 부분은 상태코드(status code)이며 플라스크에서는 기본적으로 200으로 설정합니다.
'''

# 400상태의 코드를 리턴하는데 이는 잘못된 리퀘스트 에러 코드입니다.
@app.route("/bad/")
def error():
    return '<h1>Bad Request</h1>', 400

# 응답 오브젝트를 생성하고 그 안에 쿠키를 설정하는 예입니다.
from flask import make_response
@app.route("/cookie/")
def cookie():
    response = make_response("<h1>This document carries a cookie!</h1>")
    response.set_cookie("answer", "42")
    return response

# 리다이렉트(redirect)는 페이지 도큐먼트를 포함하지 않으며 새로운 페이지를 로드하는 새로운 URL을 브라우저에 전달합니다.
# 쉽게 말해 특정 페이지로 접속하려고 하면 다른 페이지로 넘기는 것을 의미합니다.
from flask import redirect
@app.route("/re/")
def re():
    # http://127.0.0.1:5000/re 로 접속하면 bad 경로로 이동하게 됩니다.
    return redirect("/bad/")

'''
abort 함수는 에러 핸들링을 위해 사용됩니다.
from flask import abort
@app.route('/customer/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
'''

'''
2.8 플라스크 확장
- 플라스크는 데이터베이스 사용자 인증 등과 같이 중요한 기능이 의도적으로 확장이 가능하도록 설계되어 있습니다.
- 애플리케이션에 가장 적합한 패키지를 선택하거나 원하는 기능을 직접 작성할 수 있습니다.
- Flask-Script는 플라스크 애플리케이션에 커맨드 라인 파서(parser)를 추가하는 플라스크 확장입니다.
- 일반적인 목적의 옵션으로 패키징되며 커스텀 커맨드도 제공합니다.

from flask_script import Manager
manager = Manager(app)

if __name__ == "__main__":
    manager.run()

1. 커맨드창에 python hello.py 입력 : 유지보수 태스크나 테스트 혹은 디버그 이슈를 실행합니다.
2. 커맨드창에 python hello.py runserver --help 입력 : 디버그 모드에서 웹 서버를 시작하지만 사용 가능한 더 많은 옵션이 있습니다.
'''

if __name__ == "__main__":
    app.run(debug = True)
