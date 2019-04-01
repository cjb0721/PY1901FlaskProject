from orm import model
from sqlalchemy import create_engine
# 创建连接实例
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb", encoding='utf8', echo=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
session = Session()


def insertUser(name, pwd):
    session.add(model.User(username=name, password=pwd))
    session.commit()
    session.close()


def checkUser(name, pwd):
    result = session.query(model.User).filter(model.User.username==name).filter(model.User.password==pwd).first().id
    return result


def insertPro(name, body, userid):
    session.add(model.Project(proname=name, prodetail=body, userid=userid))
    session.commit()
    session.close()


def queryPro(userid):
    result = session.query(model.Project.id, model.Project.proname, model.Project.prodetail).filter(model.Project.userid==userid).all()
    return result


def queryProOne(id, userid):
    result = session.query(model.Project.id, model.Project.proname, model.Project.prodetail).filter(model.Project.userid==userid).filter(model.Project.id==id).all()
    return result


def deletePro(id, userid):
    session.query(model.Project.id).filter(model.Project.userid==userid).filter(model.Project.id==id).delete()
    session.commit()
    session.close()


def updatePro(id, body, userid):
    # result = session.query(model.Project).filter(model.Project.userid==userid).filter(model.Project.proname==name).first().name
    session.query(model.Project).filter(model.Project.userid==userid).filter(model.Project.id==id).update({"prodetail": body})
    session.commit()
    session.close()




