from bottle import auth_basic
from bottle import default_app, run
from bottle import get
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, and_, select

metadata = MetaData()
mysql_url = "mysql+mysqldb://root:@localhost:3306/shib"
engine = create_engine(mysql_url, echo=True)
conn = engine.connect()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(100)),
              Column('password', String(100))
              )
metadata.create_all(engine)


def check_auth(user, password):
    print user
    print password
    check_mess = select([users]).where(and_(
        users.c.username == user,
        users.c.password == password
    ))

    result = conn.execute(check_mess)

    if result.fetchone():
        result.close()
        return True
    result.close()
    return False


@get('/')
@auth_basic(check_auth)
def auth():
    # response.headers['WWW-Authenticate'] = 'Basic realm="Console"'
    # response.add_header('WWW-Authenticate', 'Basic realm="Papaya"')
    # abort(401, '''401 Unauthorized''')
    return "Login Success"


app = default_app()
run(app=app, host='0.0.0.0', port=8002, debug=True, reloader=True)
