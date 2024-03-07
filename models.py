from peewee import *
from datetime import date
from random import randint, uniform
import sqlite3
import json
from playhouse.postgres_ext import PostgresqlExtDatabase
database = PostgresqlExtDatabase('shipbase', user='postgres', password='sa',
                                 host='localhost', port=5432)
class BaseModel(Model):
    class Meta:
        database = database


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = database

    def __str__(self):
        return self.username
    
class Role(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    class Meta:
        database = database

    def __str__(self):
        return self.name


class UserRole(Model):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='roles',on_delete='CASCADE' )
    role = ForeignKeyField(Role, backref='users',on_delete='CASCADE')

    class Meta:
        database = database

class UserLog(Model):
    Id = AutoField(primary_key=True)
    username = CharField()
    login_time = DateTimeField()
    logout_time = DateTimeField(null=True)

    class Meta:
        database = database

class ChangedDate(Model):
    id = AutoField(primary_key=True)
    RegistryNumber = CharField()
    username = CharField()
    chenged_time = DateTimeField()
    PurchaseName = CharField(null=True)
    Role = CharField(null=True)
    Type = CharField(null=True)
    class Meta:
        database = database