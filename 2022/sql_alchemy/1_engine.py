from sqlalchemy import create_engine

url = 'sqlite:///college.db' #location/name of dtabase
engine = create_engine(url, echo = True)

