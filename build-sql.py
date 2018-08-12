from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  # 声明基类的创建类
from sqlalchemy.orm import relationship, sessionmaker

###############
'''
     创建数据库连接
'''

engine = create_engine('mysql://root:@localhost/shiyanlou', echo=True)
# print(engine.execute('show tables').fetchall())


###############
'''
     创建数据库 
'''

Base = declarative_base()    # 声明基类

class User(Base):
    '''
        创建user表
    '''
    __tablename__ = 'user'   # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(100))
    
    def __repr__(self):
        return "<User(name=%s)>" % self.name

class Course(Base):
    '''
        创建Course 表
    '''
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    teacher_id = Column(Integer, ForeignKey('user.id'))  # 设置外键
    tercher = relationship('User')

    def __repr__(self):
        return '<Course(name=%s)>' % self.name

class Lab(Base):
    '''
         创建Lab表
    '''
    __tablename__ = 'lab'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship('Course', backref='labs')
    def __repr__(self):
        return '<Lab(name=%s)>' % self.name

'''
     创建所有表
'''
Base.metadata.create_all(engine)


############################
'''
    简单CRUD操作

'''
Session = sessionmaker(bind=engine)

session = Session()


# print(session.query(User).all())

# print(session.query(User).filter(User.name=='aiden').first())

#course = session.query(Course).first()
#print(course)
#lab1= Lab(name='ORM', course_id=course.id)

#session.add(lab1)
#session.commit()
