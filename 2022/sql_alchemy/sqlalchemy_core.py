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
from sqlalchemy import join
from sqlalchemy import and_, or_
from sqlalchemy import asc, desc, between
from sqlalchemy.sql import func
from sqlalchemy import union, union_all, except_, intersect

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

# you can't  use UPDATE or I believe "Delete" with multiple tables in sqlite - skip "using multiple table updates
# also skipping parameter ordered updates

#Joins
print("#######################")
j = students.join(classes, students.c.class_id == classes.c.id)
print(j)

stmt = select([students]).select_from(j)
print(stmt)
result = conn.execute(stmt)
for row in result:
    print(row)

#AND function
print("#########################")
print("and_()")
print(and_(
students.c.name == 'Allan',
students.c.grade == 'B+'
))

stmt = select([students]).where(and_(students.c.name == "Allan", students.c.grade == "B+"))
result = conn.execute(stmt)
print(result.fetchall())

# or function
print("###########################")
print("or_()")
stmt = select([students]).where(or_(students.c.name == "Allan", students.c.grade == "B+"))
result = conn.execute(stmt)
print(result.fetchall())

# order by ascending
print("######################")
print("Sort table ascending order")
stmt = select([classes]).order_by(asc(classes.c.name))
result = conn.execute(stmt)

for row in result:
    print(row)
# Order by descending order
print("##############")
print("Sort Descending Order")
stmt = select([students]).order_by(desc(students.c.name))
result = conn.execute(stmt)
for row in result:
    print(row)

# Between
print("#######################")
print("between")
stmt = select([students]).where(between(students.c.id, 2, 4))
print(stmt)
result = conn.execute(stmt)
for row in result:
    print(row)

# Using Functions

print("########################")
print("Using functions")
print('now() = current date and time')
result = conn.execute(select([func.now()]))
print(result.fetchone())

print("count() number of rows selected in query")
result = conn.execute(select([func.count()]))
print(result.fetchone())

print("return max() value")
result = conn.execute(select([func.max(classes.c.room_num)]))
print(result.fetchone())

print("return min() value")
result = conn.execute(select([func.min(classes.c.room_num)]))
print(result.fetchone())


print("return average value")
result = conn.execute(select([func.avg(classes.c.room_num)]))
print(result.fetchone())

result = conn.execute(select([func.max(classes.c.room_num).label("name")]))

#using set operations
#preparation

addresses = Table(
"addresses", meta,
Column('id', Integer, primary_key = True),
Column('st_id', Integer),
Column('postal_add', String),
Column('email_add', String)
)
print("#############################################")
print("Union")
u = union(addresses.select().where(addresses.c.email_add.like("%gmail.com")))
print(u)
# result = conn.execute(u)
# result.fetchall() # not ran because the db is empty

print("##############")
print("Union alldoesn't remove duplicates and doesnt sort data")

u = union_all(addresses.select().where(addresses.c.email_add.like('%gmail.com')), addresses.select().where(addresses.c.email_add.like('%@yahoo.com')))
print(u)

print("############")
print("except combines select statements and returns frow from first select that are not returned by second selection")
u = except_(addresses.select().where(addresses.c.email_add.like("%gmail.com")),addresses.select().where(addresses.c.postal_add.like('%Pune')))
print(u)

print("#########################")
print("Intersection gives rows in common")
u = intersect(addresses.select().where(addresses.c.email_add.like("%gmail.com")), addresses.select().where(addresses.c.postal_add.like("%Pune")))
print(u)
