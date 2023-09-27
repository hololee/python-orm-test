'''
https://docs.sqlalchemy.org/en/20/tutorial/index.html
<기본 예제 테스트>

아래의 테이블 사용.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name character varying,
    age integer,
    sex integer,
    region character varying
);

'''
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import Session

from models import Users

engine = create_engine("postgresql://postgres:postgres@127.0.0.1:54321/db", echo=False)

metadata_obj = MetaData()

# user_table = Table(
#     "users",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("age", Integer),
#     Column("sex", Integer),
#     Column("region", String),
# ) # or.
user_table = Users.__table__

# insert test.
stmt = insert(user_table).values(name="spongebob", age=13, sex=1, region='seoul')
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

# 일반 객체로 쿼리.
stmt = select(user_table).where(user_table.c.name == "spongebob")
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

# ORM으로 쿼리.
stmt = select(Users).where(Users.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

# update test.
stmt = update(user_table).where(user_table.c.name == "spongebob").values(age=25)
with engine.connect() as conn:  # engine.connect()는 오토커밋을 지원하지 않음.
    conn.execute(stmt)
    conn.commit()
stmt = update(user_table).where(user_table.c.name == "spongebob").values(age=23)
with engine.begin() as conn:
    conn.execute(stmt)

# delete test.
stmt = delete(user_table).where(user_table.c.name == "spongebob").where(user_table.c.age == 23)
with engine.begin() as conn:
    conn.execute(stmt)
