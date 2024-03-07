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
class Ship(Model):
    id = AutoField(primary_key=True)
    reg_number = CharField(null=True)
    name = CharField(null=True)
    construction_number = CharField(null=True)
    ship_project = CharField(null=True)
    type_and_purpose = CharField(null=True)
    construction_date = DateField(null=True)
    construction_place = CharField(null=True)
    class_formula_category = CharField(null=True)
    overall_length = FloatField(null=True)
    constructive_length = FloatField(null=True)
    overall_width = FloatField(null=True)
    constructive_width = FloatField(null=True)
    freeboard = FloatField(null=True)
    side_height = FloatField(null=True)
    gross_tonnage = FloatField(null=True)
    net_tonnage = FloatField(null=True)
    deadweight = FloatField(null=True)
    displacement = FloatField(null=True)
    cargo_capacity = FloatField(null=True)
    transverse_bulkheads = IntegerField(null=True)
    longitudinal_bulkheads = IntegerField(null=True)
    passenger_capacity = IntegerField(null=True)
    crew = IntegerField(null=True)
    organization_group = CharField(null=True)
    ballast_tanks = IntegerField(null=True)
    total_tank_capacity = FloatField(null=True)
    crane_1_capacity = FloatField(null=True)
    crane_2_capacity = FloatField(null=True)
    crane_3_capacity = FloatField(null=True)
    hull_material = CharField(null=True)
    superstructure_material = CharField(null=True)
    main_engine_type = CharField(null=True)
    main_engine_model = CharField(null=True)
    main_engine_power_kw = FloatField(null=True)
    main_engine_quantity = IntegerField(null=True)
    total_engine_power_kw = FloatField(null=True)
    total_generators_kw = FloatField(null=True)
    total_auxiliary_engines_kw = FloatField(null=True)

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