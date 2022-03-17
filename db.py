from peewee import *

dbhandle = SqliteDatabase('users.db')


class Users(Model):
    chat_id = IntegerField(null=False, unique=True)
    class Meta:
        db_table = "users"
        database = dbhandle


def add_user(chat_id):
    exists = True
    try:
        user = Users.select().where(Users.chat_id == chat_id).get()
        print("User " + str(chat_id) + " exists...")
    except Exception as e:
        print(e)
        exists = False
    if exists == False:
        row = Users(
            chat_id = chat_id
        )
        row.save()
        print("User " + str(Users.get(chat_id=chat_id).chat_id) + " added...")

def get_all_users():
    chat_ids = []
    users = Users.select()
    for user in users:
        chat_ids.append(user.chat_id)
    return chat_ids
if __name__ == '__main__':
    try:
        get_all_users()
        

    except InternalError as px:
        print(str(px))