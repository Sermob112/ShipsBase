from models import *  # Замените models на имя вашего модуля или файла с определением моделей
from playhouse.postgres_ext import PostgresqlExtDatabase

# Подключение к PostgreSQL

# Подключение к системной базе данных postgres
system_db = PostgresqlDatabase('postgres', user='postgres', password='sa', host='localhost', port=5432)

# def initialize_database(db_name):
#         try:
#         # Подключаемся к системной базе данных
#             system_db.connect()

#             # Проверяем существование базы данных в системной таблице pg_database
#             query = f"SELECT datname FROM pg_database WHERE datname='{db_name}'"
#             result = system_db.execute_sql(query)
#             exists = result.rowcount > 0

#             return exists
#         except ProgrammingError:
#         # Если произошла ошибка, вероятно, базы данных с указанным именем не существует
#             return False
#         finally:
#             # Всегда закрываем соединение с системной базой данных
#             system_db.close()
# # Вызываем функцию инициализации базы данных
# if not initialize_database("ShipBase"):
def initialize_database():
    try:
        system_db.execute_sql("CREATE DATABASE shipbase")
        db = PostgresqlDatabase('shipbase', user='postgres', password='sa', host='localhost', port=5432)
        db.create_tables([User,Role,UserRole,UserLog,ChangedDate], safe=True)
        admin_user = User.create(username='Якупов', password='1')
        readactor = User.create(username='Померанец', password='2')
        regular_user = User.create(username='Маковий', password='3')
        gost = User.create(username='Ваучский', password='4')
        admin_role = Role.create(name='Администратор')
        readactor_role = Role.create(name='Редактор')
        user_role = Role.create(name='Пользователь')
        gost_role = Role.create(name='Гость')
        UserRole.create(user=regular_user, role=user_role)
        UserRole.create(user=admin_user, role=admin_role)
        UserRole.create(user=readactor, role=readactor_role)
        UserRole.create(user=gost, role=gost_role)
        system_db.close()
    except Exception as E:
        print(E)