### sqlite3 ORM <br>
##### Usage and requirements
First set the path to database in file [/src/share/conf.ini](/share/conf.ini) in "db_settings" section.<br>
By default ORM creates database in the same folder with name "testORM.db".<br>
Examples of usage are shown in file [src/sqlite3_ORM/base.py](/src/sqlite3_ORM/base.py) <br>
Simple table creating:
```
class User(Base):

    __tablename__ = 'users'

    id = ('int', 'not null', 'pk')
    username = ('varchar(256)', 'not null')
```
To create a new table, call the create() method:
```
User().create()
```
Method names are like what you want to get:
```
user = User.filter(id=2)
user.update(name='Updated')
user.delete()
```
To see all available methods, look at the Base class methods in the file [/src/sqlite3_ORM/pdbc.py](/src/sqlite3_ORM/pdbc.py)



