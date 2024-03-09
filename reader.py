
import csv, json
import datetime
import pandas as pd
import os
import sqlite3
from models import *


# database = PostgresqlExtDatabase('shipbase', user='postgres', password='sa',
#                                  host='localhost', port=5432)
def insert_in_table(csv_file_path):
    errors = []
    inserted_rows = 0 
    try:
        with open(csv_file_path, 'r', encoding='windows-1251') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ';')
            next(csv_reader)  # Пропустите заголовок, если он есть
        
            for row in csv_reader:
                
                reg_number = row[0] if row[0] else 'Нет данных'
                name = row[1] if row[1] else 'Нет данных'
                construction_number = row[2] if row[2] else 'Нет данных'
                ship_project = row[3]if row[3] else 'Нет данных'
                type_and_purpose = row[4]if row[4] else 'Нет данных'
                construction_date = row[5] if row[5] else 'Нет данных'
                try:
                    construction_date = datetime.datetime.strptime(construction_date, '%d.%m.%Y').date()
                except ValueError:
                    construction_date = None
                construction_place = row[6] if row[6] else None
                class_formula_category = row[7] if row[7] else None
                overall_length = float(row[8]) if row[8] else None
                constructive_length = float(row[9]) if row[9] else None
                overall_width = float(row[10]) if row[10] else None
                constructive_width = float(row[11]) if row[11] else None
                freeboard = float(row[12]) if row[12] else None
                side_height = float(row[13]) if row[13] else None
                gross_tonnage = float(row[14]) if row[14] else None
                net_tonnage = float(row[15]) if row[15] else None
                deadweight = float(row[16]) if row[16] else None
                displacement = float(row[17]) if row[17] else None
                cargo_capacity = float(row[18]) if row[18] else None
                transverse_bulkheads = int(row[19]) if row[19] else None
                longitudinal_bulkheads = int(row[20]) if row[20] else None
                passenger_capacity = int(row[21]) if row[21] else None
                crew = int(row[22]) if row[22] else None
                organization_group = row[23] if row[23] else None
                ballast_tanks = int(row[24]) if row[24] else None
                total_tank_capacity = float(row[25]) if row[25] else None
                crane_1_capacity = float(row[26]) if row[26] else None
                crane_2_capacity = float(row[27]) if row[27] else None
                crane_3_capacity = float(row[28]) if row[28] else None
                hull_material = row[29] if row[29] else None
                superstructure_material = row[30] if row[30] else None
                main_engine_type = row[31] if row[31] else None
                main_engine_model = row[32] if row[32] else None
                main_engine_power_kw = float(row[33]) if row[33] else None
                main_engine_quantity = int(row[34]) if row[34] else None
                total_engine_power_kw = float(row[35]) if row[35] else None
                total_generators_kw = float(row[36]) if row[36] else None
                total_auxiliary_engines_kw = float(row[37]) if row[37] else None

                Ship.create(
                reg_number=reg_number,
                name=name,
                construction_number=construction_number,
                ship_project=ship_project,
                type_and_purpose=type_and_purpose,
                construction_date=construction_date,
                construction_place=construction_place,
                class_formula_category=class_formula_category,
                overall_length=overall_length,
                constructive_length=constructive_length,
                overall_width=overall_width,
                constructive_width=constructive_width,
                freeboard=freeboard,
                side_height=side_height,
                gross_tonnage=gross_tonnage,
                net_tonnage=net_tonnage,
                deadweight=deadweight,
                displacement=displacement,
                cargo_capacity=cargo_capacity,
                transverse_bulkheads=transverse_bulkheads,
                longitudinal_bulkheads=longitudinal_bulkheads,
                passenger_capacity=passenger_capacity,
                crew=crew,
                organization_group=organization_group,
                ballast_tanks=ballast_tanks,
                total_tank_capacity=total_tank_capacity,
                crane_1_capacity=crane_1_capacity,
                crane_2_capacity=crane_2_capacity,
                crane_3_capacity=crane_3_capacity,
                hull_material=hull_material,
                superstructure_material=superstructure_material,
                main_engine_type=main_engine_type,
                main_engine_model=main_engine_model,
                main_engine_power_kw=main_engine_power_kw,
                main_engine_quantity=main_engine_quantity,
                total_engine_power_kw=total_engine_power_kw,
                total_generators_kw=total_generators_kw,
                total_auxiliary_engines_kw=total_auxiliary_engines_kw
                     )
                inserted_rows += 1
        # inserted_rows = len([record for record in Ship.select()])

    except Exception as e:
        errors.append(str(e))  # Добавьте ошибку в список ошибок
    # finally:
    #     database.close()
    return inserted_rows, errors

    
def count_total_records():
    total_records = Ship.select().count()

    return total_records
# insert_in_table('Файлы отладки.csv')