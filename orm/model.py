
class Test:

    def __init__(self, id):
        self.id = id

"""
    ORM 生成数据库中的表
"""
from sqlalchemy import create_engine
# 创建连接实例
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb", encoding='utf8', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)

from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(40), nullable=False)


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # proname = Column(String(40), nullable=False, unique=True)
    proname = Column(String(40), nullable=False)
    prodetail = Column(String(200))
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)


