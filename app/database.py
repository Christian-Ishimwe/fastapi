import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker
from .config import  settings
SQLALCHEMY_DATABASE_URL=f"""postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"""
engine=create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base=declarative_base()


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    
while True:
    try:
        conn=psycopg2.connect(host='localhost', password='christian', user='postgres',database='fastapi', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('successful connected')
        break
    except Exception as error:
        
        print('failed to auntantivate')
        print('error is', error)
        time.sleep(2)