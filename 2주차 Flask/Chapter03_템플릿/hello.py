'''
Chapter03 템플릿

- 비즈니스 로직 : 특정한 값을 얻기 위해 데이터의 처리를 수행하는 응용 프로그램의 일부 (백엔드)
- 프레젠테이션 로직 : 말 그대로 보여주기 위한 로직 (response를 브라우저에 전송)
'''

'''
3.1 Jinja2 템플릿 엔진

3.1.1 템플릿 렌더링
- 템플릿은 프레젠테이션 로직을 모아놓아 비즈니스 로직과 프레젠테이션 로직의 혼동을 구분하는데 효과적입니다.
- 렌더링(Rendering) : 코드를 웹 브라우저에 구현하는 것을 의미합니다(?)
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/index/")
def index():
    return render_template("index.html")

@app.route("/user/<username>/")
def user(username):
    return render_template("user.html", name = username)


'''
3.1.2 변수
- 템플릿에선 변수를 {{변수명}} 형태로 지정합니다.
- 템플릿 엔진에 요청해 템플릿이 렌더링되는 시점에서 제공되는 데이터로부터 얻어 오는 값을 의미합니다.
- Jinja2는 어떠한 타입의 변수라도 인식합니다.

- Jinja2 변수 필터
1. safe : 이스케이프를 적용하지 않고 값을 렌더링합니다.
2. capitalize : 값의 첫 번째 문자를 대문자로 만들고 나머지는 소문자로 만듭니다.
3. lower : 값을 소문자로 만듭니다.
4. upper : 값을 대문자로 만듭니다.
5. title : 값의 각 단어들을 capitalize합니다.
6. trim : 앞부분과 뒷부분에서 공백 문자를 삭제합니다.
7. striptags : 렌더링하기 전에 값에 존재하고 있는 HTML 태그를 제거합니다.
'''

'''
3.1.3 제어구조
{% : 템플릿에서의 프로그래밍 영역을 넣기 위해 시작하는 기호 (Block_start_string)
%} : 프로그래밍 영역 기술을 끝내고 프로그래밍 영역을 종료하는 기호 (Block_end_string)

{{ : 변수를 출력하기 위해 시작하는 기호 (Variable_start_string)
}} : 변수 출력이 끝나고 나서 사용하는 기호 (Variable_end_string)

{# : 주석을 넣기 위해 시작하는 기호 (comment_start_string)
#} : 주석을 넣고 종료하기 위해 사용하는 기호 (comment_end_string)

- Jina2는 매크로(macro)를 제공하는데 이는 파이썬 코드의 함수라고 생각하면 됩니다.
- 매크로를 재사용하기 위해선 독립적인 파일에 저장하고 필요할 때 템플릿에 import하는게 편합니다.

- 재사용의 또 다른 강력한 기능은 템플릿의 상속에 있습니다.
- 파이썬의 클래스 상속과 비슷한 개념입니다.
'''


'''
3.2 Flask-Bootstrap과 트위터 부트스트랩의 통합
- 부트스트랩은 트위터에서 제공하는 오픈 소스 프레임워크입니다.
- 클라이언트 측의 프레임워크이므로 서버를 포함하고 있지 않습니다.
- 부트스트랩과 애플리케이션을 통합하는 가장 확실한 방법은 템플릿에 필요한 모든 변경사항들을 만들어두는 것입니다.
- 더 간단한 방법은 Flask-Bootstrap이라고 하는 플라스크 확장을 사용하면 됩니다.

- Flask-Bootstrap의 베이스 템플릿 블록들
01. doc : 전체 HTML 문서
02. html_attribs : <html> 태그 안에 있는 속성들
03. html : <html> 태그의 콘텐츠
04. head : <head> 태그의 콘텐츠
05. title : <title> 태그의 콘텐츠
06. metas : <meta> 태그의 콘텐츠
07. styles : CSS 정의
08. body_attribs : <body> 태그의 속성
09. body : <body> 태그의 콘텐츠
10. navbar : 사용자 정의 내비게이션 바
11. content : 사용자 정의 페이지 콘텐츠
12. scripts : 문서 아랫부분의 자바스크립트 선언
'''

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


'''
3.3 커스텀 에러 페이지
- 플라스크에서는 애플리케이션에서 일반적인 라우트와 마찬가지로 템플릿에 기반을 둔 커스텀 에러 페이지를 정의할 수 있도록 해줍니다.

- 대표적인 에러 코드
1. 404코드 : 클라이언트가 알지 못하는 페이지나 경로를 요청했을 때 발생합니다.
2. 500코드 : 처리하지 못하는 예외에 대해서 발생합니다
'''

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


'''
넘어가기 전에 정리!

1. template 폴더를 통해 비즈니스 로직을 정리하고 있습니다.
2. 기본이 되는 템플릿은 base.html입니다. 여기서 부트스트랩을 불러와({extends bootstrap/base.html}) 커스터마이징을 진행했습니다. (뼈대를 만듭니다.)
3. user.html, 404.html, 500.html을 기본적으로 base.html의 구조를 가져왔습니다. (상속을 받아옵니다.)
4. 이 구조를 불러와({extends base.html}) 각 페이지의 목적에 맞는 내용을 작성합니다.
5. 이를 render_template을 통해 불러와 애플리케이션을 실행합니다.
'''


'''
3.4 링크
- 하나 이상의 라우터가 필요한 애플리케이션은 내비게이션 바와 같이 서로 다른 페이지들을 연결하는 링크를 포함시켜야 합니다.
- 템플릿에 직접 링크하는 것처럼 URL을 작성하는 것은 간단한 라우트 방법이지만 동적 라우트를 위해 템플릿에서 URL을 구성하는 것은 복잡합니다.

- 직접 작성한 URL은 코드에 정의된 라우트와 원하지 않은 의존성을 생성할 수도 있습니다.
- 이러한 문제를 피하기 위해 플라스크가 url_for() 헬퍼 함수를 제공합니다.
- 이 함수는 애플리케이션 URL 맵에 저장된 정보를 통해 URL을 생성합니다.
'''


'''
3.5 정적 파일
- 대부분의 애플리케이션은 HTML 코드에서 참조되는 이미지, 자바스크립트 소스파일, CSS 파일과 같은 정적 파일들을 사용합니다.
- 정적파일에 대한 참조는 '/static/<filename>'과 같이 특별한 경로로 정의되어 처리됩니다.
'''


'''
3.6 Flask-Moment를 이용한 날짜와 시간 지역화
- 각 나라마다 시간대가 다르기 때문에 웹 애플리케이션에서 날짜와 시간을 처리하는 것은 간단한 문제가 아닙니다.
- 서버는 각 사용자의 위치와 무관한 일정한 시간 단위가 필요했고 그래서 생겨난 것이 협정세계시(Corrdinated Universial Time, UTC)를 사용합니다.

- 하지만 사용자는 UTC를 이해하는 것이 없기 때문에 자신의 나라에 맞는 시간을 렌더링해서 보여줄 필요가 있습니다.
- 이를 위해 Flask-moment를 활용합니다. Flask-moment는 moment.js와 jquery.js가 필요합니다.
- 부트스트랩은 jquery.js를 포함하고 있기 때문에 moment.js만 추가하면 됩니다.
'''

from flask_moment import Moment
moment = Moment(app)

from datetime import datetime

@app.route("/date/")
def date():
    return render_template("index2.html", current_time = datetime.utcnow())



if __name__ == "__main__":
    app.run(debug = True)
