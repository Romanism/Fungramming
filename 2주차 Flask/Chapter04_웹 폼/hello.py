'''
Chapter04 웹 폼

- 플라스크의 리퀘스트 오브젝트에서 제공하는 지원이 웹 폼을 처리하기에 충분합니다.
- 하지만 간단하지만 반복적인 일들이 여럿 존재합니다.
- 폼을 형성하는 HTML 코드의 생성과 서브밋한 폼 데이터의 검증이 좋은 예입니다.
'''


'''
4.1 크로스-사이트 리퀘스트 위조(CSRF) 보호
- CSRF 공격은 악의적 웹사이트에서 희생자가 로그인한 다른 웹 사이트로 리퀘스트를 전송할 때 일어납니다.
- 기본적으로 Flask-WTF는 CSRF 공격으로부터 모든 폼을 보호합니다.

- CSRF 보호를 구현하기 위해서 Flask-WTF는 암호화 키를 설정하기 위한 애플리케이션이 필요합니다.
- Flask-WTF는 이 키를 사용해 암호화된 토큰을 생성하고 이 토큰은 폼 데이터와 함께 리퀘스트 인증을 검증하는데 사용합니다.
'''

from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)

# app.config : 프레임워크, 확장 혹은 애플리케이션 자체에서 사용하는 설정 변수들을 저장하기 위해 일반적으로 사용하는 공간입니다.
# SECRET_KEY : 플라스쿠와 여러 서드 파티 확장에서 일반적인 암호화키로 사용됩니다.
# 보안성을 향상 시키기 위해선 보안 키를 코드 내에 삽입하는 것보다 환경변수에 저장하는게 좋습니다. (7장에서 설명)
app.config["SECRET_KEY"] = "hard to guess string"


'''
4.2 폼 클래스
- Flask-WTF를 사용할 때 각 웹 폼은 Form 클래스로부터 상속한 클래스에 의해 표현됩니다.
- 클래스는 폼에 있는 필드의 리스트를 정의하는데, 이 필드는 각각 오브젝트로 표현됩니다.
- 각 필드 오브젝트는 하나 이상의 검증자(validator)가 붙어 있습니다.
- 검증자는 사용자가 서브밋한 입력값이 올바른지 체크하는 함수입니다.
'''

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField("What Is Your Name?", validators = [Required()])
    submit = SubmitField("Submit")

'''
4.3 폼의 HTML 렌더링
- 폼 필드가 호출되면 템플릿은 HTML로 렌더링 됩니다.
- Flask-Bootstrap은 전체 Flask-WTF 폼을 렌더링하기 위해 부트스트랩의 미리 정의된 폼 스타일을 사용하도록 함수를 제공합니다.
- 이를 불러오는 방법이 한번의 호출로 이루어 집니다.

{% import "bootstrap/wtf.html" as wtf %}
{{wtf.quick_form(form)}}
'''

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)

'''
@app.route("/", methods = ["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template("index.html", form = form, name = name)
'''


'''
4.4 리다이렉트와 사용자 세션

- 4.3까지 완료한 후에 입력창에 이름을 입력하고 새로고침을 하면 에러가 발생합니다.
- 그 이유는 새로고침 할 때 전송되는 마지막 리퀘스트를 반복하기 때문에 생깁니다.
- 따라서 웹 애플리케이션이 브라우저에 의해 전송된 마지막 리퀘스트로 POST 리퀘스트를 남겨 두지 않도록 습관을 들이는게 좋습니다.


# 올바른 폼 데이터와 함께 전송된 리퀘스트는 redirect()를 호출하여 끝맺습니다.
# 이 redirect() 함수는 헬퍼 함수이며 인수로 리다이렉트할 URL을 받습니다.
@app.route("/", methods = ["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", form = form, name = session.get("name"))
'''


'''
4.5 메시지 플래싱
- 플래싱은 리퀘스트를 완료하고 나서 사용자에게 상태 업데이트를 전달하는 것을 의미합니다.
- 예를 들어 로그인 시 패스워드를 잘못 입력하면 패스워드가 틀렸다는 정보를 알려주는 메시지를 로그인 폼에 다시 렌더링하도록 응답해야 합니다.
'''

@app.route("/", methods = ["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!!")
        session["name"] = form.name.data
        form.name.data = ''
        return redirect(url_for("index"))
    return render_template("index.html", form = form, name = session.get("name"))

if __name__ == "__main__":
    app.run(debug=True)
