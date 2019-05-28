#! /usr/bin/env python3

from pdbc import Base


class Post(Base):

    __tablename__ = 'posts'

    id = ('int', 'not null', 'pk')
    text = ('text', 'not null')
    user_id = ('int', 'not null')

    FK = [('user_id', 'users.id')]


class User(Base):

    __tablename__ = 'users'

    id = ('int', 'not null', 'pk')
    username = ('varchar(256)', 'not null')


User().create(echo=True)
a = User()
a.id = 1
a.username = 'cccc'
a.save(echo=True)

b = User()
b.id = 2
b.username = 'test'
b.save(echo=True)

Post().create(echo=True)
p = Post()
p.id = 1
p.text = 'some simple text'
p.user_id = '1'
p.save(echo=True)

p = Post()
p.id = 2
p.text = 'U will never see this text'
p.user_id = '2'
p.save(echo=True)
print()
print("Filtered post:\n")
filtered_post = Post().filter(id=2)
print(filtered_post)
print()

print("Updated post:\n")
filtered_post.update(text='Updated post text of id == 2', echo=True)
out = Post().filter(id=2, echo=True)
print(out)
print()

print("Filtered user:\n")
filtered_user = User().filter(id=2)
print(filtered_user)
print()

print("Updated user:\n")
filtered_user.update(username='Updated', echo=True)
out = User().filter(id=2, echo=True)
print(out)
print()

print("All users:\n")
all = User().select_all(echo=True)
print(all)
print()

print("Users with Posts:\n")
all = User().select_with(Post, echo=True)
print(all)
print()

print("Users with Posts on condition:\n")
all = User().select_with(Post, condition="users.id == posts.id", echo=True)
print(all)
print()

print("All users after deleting one:\n")
user_to_delete = User().filter(id=2)
user_to_delete.delete(echo=True)
all = User().select_all(echo=True)
print(all)
print()

print("All users befor deleting all:\n")
c = User()
c.id = 22
c.username = 'aftertest'
c.save(echo=True)
all = User().select_all(echo=True)
print(all)
print()

User().delete_all(echo=True)
all = User().select_all(echo=True)
print(all)

print('\n END')
