from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin,LoginManager,login_user,current_user,logout_user,login_required
Base=declarative_base()

class Register(Base):
	__tablename__='register'

	id=Column(Integer,primary_key=True)
	name=Column(String(100))
	surname=Column(String(100))
	mobile=Column(String(20))
	email=Column(String(50))
	branch=Column(String(10))
	roll=Column(String(50))

class User(Base,UserMixin):
   __tablename__='user'

   id=Column(Integer,primary_key=True)
   name=Column(String(100),nullable=False)
   
   email=Column(String(50),nullable=False)
   password=Column(String(10),nullable=False)

engine=create_engine('sqlite:///iiit.db')
Base.metadata.create_all(engine)
print("Database Created")