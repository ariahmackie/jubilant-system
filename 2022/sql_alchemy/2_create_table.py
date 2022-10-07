# 1. Import create_engine, metadata, table, column, and data types
# 2. create your engine
# 3. Create your meta data object
# 4. Create your table with its name, its metadata object, and its designated columns
# 5. Call meta.create_all method.


import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy import text
from sqlalchemy.sql import alias

#Delete a Database
os.remove("lotr.db")
os.remove("college.db")
# Create Engine
engine = create_engine('sqlite:///lotr.db', echo = True)
meta = MetaData()

# Create a Table
hobbits = Table(
	'Hobbits', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String),
	Column('lastname', String),
	)

meta.create_all(engine)

conn = engine.connect()

# Insert 1 Hobbit
insert = hobbits.insert().values(name = "Rosey", lastname = 'Cotton')
result = conn.execute(insert)
print(result.inserted_primary_key)

#insert a dictionary of students
conn.execute(hobbits.insert(), [
{'name': 'Frodo', 'lastname' : 'Baggins'},
{'name': 'Samwise', 'lastname' : 'Gamgee'},
{'name': 'Meriadoc', 'lastname' : 'Brandybuck'},
{'name': 'Peregrin', 'lastname' : 'Took'},
])

#Select Rows
select_hobbits = hobbits.select()
result = conn.execute(select_hobbits)
row = result.fetchone()

for row in result:
	print(row)

#Select with a 'where" condition
select_hobbits = hobbits.select().where(hobbits.c.id>2)
result = conn.execute(select_hobbits)
row = result.fetchone()

for row in result:
	print(row)

# using select
s = select([hobbits])
result = conn.execute(s)

#textual SQL, for when you just want to write plain SQL
print("Textual SQL")
t = text("SELECT * FROM Hobbits")
result = conn.execute(t)
row = result.fetchone()
for row in result:
	print(row)

# textual SQL with Bound paramaters - one way to do this, there are others
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_using_aliases.htm
print("######################")
print("textual SQL with bound parameters")
s = text("select hobbits.name, hobbits.lastname from hobbits where hobbits.name between :x and :y")
result = conn.execute(s, x = 'C', y = 'G')
row = result.fetchone()
for row in result:
	print(row)

# Alias example - giving a table a temporary name that is more conveinant or readable
print("###################")
print("Alias example")
h = hobbits.alias("hob")
query = select([h]).where(h.c.id >2)

# This is SELECT stud.id, stud.name, stud.lastname FROM Students WHERE stud.id > 1
result = conn.execute(query)
for row in result:
	print(row)

# Update example
#table.update().where(conditions).values(SET expressions)
print("##################################")
print("Update Example.")
query = hobbits.update().where(hobbits.c.lastname == 'Took').values(lastname = 'T')
conn.execute(query)
query2 = hobbits.select()
result = conn.execute(query2) 

row = result.fetchone()
for row in result:
	print(row)

# Delete Example
print("##################################3")
print("Delete Example")
stmt = hobbits.delete().where(hobbits.c.name == 'Frodo')
conn.execute(stmt)
selection = hobbits.select()
result = conn.execute(selection)
row = result.fetchone()
for row in result:
	print(row)

# Using Many Tables

print("#############################")
print("Using Multiple Tables")
engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()
conn = engine.connect()
students = Table(
	'students', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String),
	Column('lastname', String),
	Column('grade', String),
	Column('class_id', Integer, ForeignKey("classes.id"))
)

classes = Table(
	'classes', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String),
	Column('room_num', Integer),
)

meta.create_all(engine)

conn.execute(classes.insert(), [
{'name': 'world history', 'room_num': 12},
{'name': "theater", 'room_num': 13},
{'name': 'math 1', 'room_num': 25},
{'name': 'chem 2', 'room_num': 31}

])

conn.execute(students.insert(), [
{'name': 'Bob', 'lastname': 'Oswald', 'grade': 'B+', 'class_id': 1},
{'name': 'Allan', 'lastname': 'A', 'grade' : 'A-', 'class_id': 2},
{'name': 'Rebecca', 'lastname': 'V', 'grade': 'C',  'class_id': 3},
])


s = select([students, classes]).where(classes.c.id==students.c.class_id)
result = conn.execute(s)
for row in result:
	print(row)

# you can't  use UPDATE with multiple tables in sqlite - skip "using multiple table updates

#parameter ordered updates 
print("####################################")
print("Parameter Ordered Updates")

