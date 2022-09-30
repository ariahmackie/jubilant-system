# 1. Import create_engine, metadata, table, column, and data types
# 2. create your engine
# 3. Create your meta data object
# 4. Create your table with its name, its metadata object, and its designated columns
# 5. Call meta.create_all method.



from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

engine = create_engine('sqlite:///example.db', echo = True)
meta = MetaData()

# create students table
students = Table(
	'students', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String),
	Column('lastname', String),
)

#create player table
players = Table(
	'players', meta,
	Column('id', Integer, primary_key = True),
	Column('username', String),
	Column('email', String),
	Column('password', String),
	)

meta.create_all(engine)

conn = engine.connect()

# Insert 1 student
insert = students.insert().values(name = "Sam", lastname = 'Peterson')
result = conn.execute(insert)
print(result.inserted_primary_key)

#insert a dictionary of students
conn.execute(students.insert(), [
{'name': 'Frodo', 'lastname' : 'Baggins'},
{'name': 'Samwise', 'lastname' : 'Gamgee'},
{'name': 'Meriadoc', 'lastname' : 'Brandybuck'},
{'name': 'Peregrin', 'lastname' : 'Took'},
])

