from peewee import *

dbhandle = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = dbhandle
 
 
class User(BaseModel):
    chat_id = IntegerField(null=False)
 
    class Meta:
        db_table = "users"
        order_by = ('chat_id',)


def add_user(chat_id):
    exists = False
    try:
        User.select().where(User.chat_id == chat_id)
        print("User " + str(chat_id) + " exists...")
    except:
        exists = True
    if exists:
        row = User(
            chat_id = chat_id
        )
        row.save()
        print("User " + chat_id + " added...")


if __name__ == '__main__':
    try:
        dbhandle.connect()
        User.create_table()
    except peewee.InternalError as px:
        print(str(px))