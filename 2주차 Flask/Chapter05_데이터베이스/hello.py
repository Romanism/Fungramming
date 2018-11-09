'''
Chapter05 데이터베이스

- 데이터베이스는 구조적인 방법으로 애플리케이션 데이터를 저장합니다.
- 애플리케이션은 필요한 특정 데이터를 추출하기 위해 쿼리(query)를 실행합니다.
- 일반적으로 데이터베이스에서 공통적으로 사용되는 것은 관계형 모델이며 이를 SQL(Structured Query Language) 데이터베이스라고 합니다.
- 최근에는 NoSQL 데이터베이스로 대중화되고 있습니다.
- NoSQL은 문서-기반과 키-값 데이터베이스를 사용합니다.
'''


'''
5.1 SQL 데이터베이스
- 관계형 데이터베이스는 테이블(Table)에 데이터를 저장하며 애플리케이션 도메인에 따라 다른 엔터티를 모델링합니다.
- 테이블은 고정된 수의 열과 변경 가능한 행으로 구성됩니다.
- 열은 테이블에서 표현된 엔터티의 데이터 속성을 정의하고 행은 실제 데이터 항목을 정의합니다.

- 테이블은 기본키(primary_key)을 가지고 있는데 이는 각 행을 위해 유일한 인식자를 의미합니다.
- 외래키(foreign_key)는 같거나 다른 테이블에서 다른 열의 기본키를 참조합니다.
- 열 사이의 링크를 관계(Relationship)라 하는데 이는 관계형 데이터베이스 모델의 기본이 됩니다.
- 관계 데이터베이스 엔진은 필요할 때 테이블들 사이에 조인 오퍼레이션을 수행하도록 지원합니다.
'''


'''
5.2 NoSQL 데이터베이스
- 관계형 모델을 따르지 않는 데이터베이스를 NoSQL 데이터베이스라고 합니다.
- NoSQL 데이터베이스의 공통된 구조는 테이블을 대신해 컬렉션과 레코드 대신 도큐먼트를 사용한다는 점입니다.
- NoSQL은 조인이 어려워 대부분 이러한 오퍼레이션을 전혀 사용하지 않습니다.

- 데이터가 중복되면 더 빠르게 쿼리를 실행 할 수 있습니다.
- 사용자와 사용자 규칙은 조인이 필요 없기 때문에 직관적입니다.
'''


'''
5.3 Flask-SQLAlchemy를 이용한 데이터베이스 관리
- Flask-SQLAlchemy는 플라스크 애플리케이션 안에 있는 SQLAlchemy의 사용을 간단하게 하는 플라스크 확장입니다.
- SQLAlchemy는 여러 데이터베이스 백엔드를 지원하는 강력한 관계형 데이터베이스 프레임워크입니다.
'''

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 클래스 SQLAlchemy에서 인스턴스화된 db 오브젝트는 데이터베이스를 표현하며 Flask-SQLAlchemy에 대한 모든 기능을 엑세스 할 수 있도록 제공합니다.
db = SQLAlchemy(app)


'''
5.4 모델 정의 (파이썬의 클래스)

- 모델(model)은 애플리케이션에서 사용되는 영구적인 엔터티를 참조할 때 사용됩니다.
- ORM의 컨텍스트에서 모델은 일반적으로 대응되는 데이터베이스 테이블의 열과 매칭되는 속성을 갖는 파이썬 클래스를 의미합니다.
- Flask-SQLAlchemy는 모든 모델에서 기본키 열을 설정하도록 해야 하며 그 키는 일반적으로 id가 됩니다.

class Role(db.Model):
    # tablename의 클래스 변수는 DB에 있는 테이블 이름을 정의합니다.
    __tablename__ = "roles"
    # 남아있는 클래스 변수들은 모델의 속성이며 db.Column 클래스의 인스턴스로 정의됩니다.
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    # tablename의 클래스 변수는 DB에 있는 테이블 이름을 정의합니다.
    __tablename__ = "users"
    # 남아있는 클래스 변수들은 모델의 속성이며 db.Column 클래스의 인스턴스로 정의됩니다.
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)

    def __repr__(self):
        return '<User %r>' % self.username
'''


'''
5.5 관계
- 관계형 데이터베이스는 관계를 통해 서로 다른 테이블의 행들을 연결합니다.
- 일대다 관계가 어떻게 모델 클래스를 표현하는지 확인해보겠습니다.

- 일반적인 SQLAlchemy 관계 옵션
1. backref : 관계에서 다른 모델에 있는 백 레퍼런스(back reference)를 추가합니다.
2. primaryjoin : 두 개 모델 사이의 join 조건을 명확하게 설정합니다.
3. lazy : 관계된 아이템이 어떻게 로드되는지를 설정합니다. (select, immediate, joined, subquery, noload, dynamic)
4. uselist : Flase로 설정하면 리스트 대신 스칼라를 사용합니다.
5. order_by : 관계에서 아이템을 위해 사용되는 순서로 설정합니다.
6. secondary : 다대다 관계에서 사용하기 위해 관계 테이블의 이름을 설정합니다.
7. secondaryjoin : SQLAlchemy가 결정하지 못할 때 다대다 관계를 위한 두번째 조인 조건을 설정합니다.
'''

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    # 관계의 오브젝트-기반 뷰를 표현합니다.
    # Role 클래스의 인스턴스로 주어진 user 속성은 그 규칙과 연관된 사용자의 리스트를 리턴합니다.
    # db.relationship()의 첫번째 인수는 관계의 다른쪽에 어떤 모델이 있는지를 확인합니다.
    # db.relationship()에 대한 backref 인수는 User 모델에 role 속성을 추가하여 관계의 방향을 정의합니다.
    # 이 속성은 Role 모델이 외래키 대신 오브젝트에 접근하도록 role_id 대신에 사용됩니다.
    # 쿼리가 자동으로 실행되지 않도록 리퀘스트하기 위해 lazy = 'dynamic'인수로 지정합니다.
    users = db.relationship("User", backref = "role", lazy = "dynamic")
    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    # User 모델에 추가된 role_id는 외래키로 정의되는데 이는 관계를 형성합니다.
    # db.ForeignKey()에 전달한 roles.id 인수는 열이 roles 테이블에 있는 행에서 id 값을 갖는 것을 의미합니다.
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return '<User %r>' % self.username


'''
5.6 데이터베이스 오퍼레이션
- ipython 파일로 제공하고 있습니다.
'''


'''
5.7 뷰 함수에서 데이터베이스의 사용
- 사용자가 입력한 이름을 저장하는 홈페이지 라우트의 새로운 버전을 보여줍니다.
'''

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
app.config["SECRET_KEY"] = "hard to guess string"

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)

class NameForm(Form):
    name = StringField("What Is Your Name?", validators = [Required()])
    submit = SubmitField("Submit")

@app.route("/", methods = ["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session["Known"] = False
        else:
            session["Known"] = True

        session["name"] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template("index.html", form = form, name = session.get("name"),
                            Known = session.get("known", False))


'''
5.8 파이썬 쉘을 이용한 통합
- 쉘 세션이 시작될 때마다 데이터베이스 인스턴스와 모델을 임포트하는건 귀찮습니다.
- 임포트의 반복을 피하기 위해 Flask-Script의 쉘 커멘트를 이용합니다.
- 임포트 리스트에 오브젝트를 추가하기 위해 쉘 커맨드는 make_context 콜백 함수를 이용해 등록해야 합니다.
'''

# make_shell_context() 함수는 애플리케이션과 데이터베이스 인스턴스, 모델을 등록합니다.
# 이것들은 자동으로 쉘에 임포트됩니다.
from flask_script import Shell, Manager
manager = Manager(app)

def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role)

manager.add_command("shell", Shell(make_context = make_shell_context))


'''
5.9 Flask-Migrage를 이용한 데이터베이스 마이그레이션
- 애플리케이션 개발 과정에서 데이터베이스 모델을 변경하거나 데이터베이스를 업데이트해야 할 경우가 종종 있을겁니다.
- 하지만 Flask-SQLAlchemy의 경우는 테이블을 업데이트하기 위해선 이전 테이블을 삭제해야 하는 단점이 있습니다.
- 이를 해결하기 위해 데이터베이스 마이그레이션 프레임워크를 활용합니다.
- 마이그레이션은 데이터베이스 스키마(schema)의 변경을 추적해 추가된 변경 사항을 데이터베이스에 적용합니다.

- Alembic에서 데이터베이스 마이그레이션은 마이그레이션 스크립트로 표현됩니다.
- 이 스크립트는 upgrade()와 Downgrade()라는 두개의 함수를 갖고 있습니다.
1. upgrade() : 마이그레이션의 부분으로 데이터베이스 변경을 적용합니다.
2. downgrade() : 삭제하는 역할을 합니다.

- 마이그레이션 스크립트를 일단 검토하고 받아들이면, 스크립트는 db upgrade 커맨드를 사용하여 데이터베이스에 적용됩니다.
'''

from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
# 데이터베이스 마이그레이션 커맨드를 보여주기 위해 MigrateCommand 클래스를 보여줍니다.
# 이 예제에서 커맨드는 db를 사용합니다.
manager.add_command("db", MigrateCommand)

# migration을 실행하기 위해선 manager.run()을 실행합니다.
if __name__ == "__main__":
    app.run()
    # manager.run()
