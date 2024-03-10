from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QStringListModel,Signal
from PySide6.QtGui import *
from peewee import *
import pandas as pd
from models import Ship
import json
from functools import partial
ships = Ship.select()  # Предположим, что здесь вы делаете запрос к вашей модели Ship
df = pd.DataFrame([(ship.ship_project, ship.id) for ship in ships], columns=['Проект', 'Ед'])
pivot_table = df.pivot_table(index='Проект', aggfunc='size', fill_value=0).reset_index()
pivot_table.columns = ['Проект', 'Ед']  # Называем столбцы после создания сводной таблицы

total_ship_counts = pivot_table['Ед'].sum()  # Применяем sum() только к столбцу 'Ед'

# Создаем DataFrame из суммы
total_ship_counts = pd.DataFrame({'Суммы': [total_ship_counts]})
total_ship_counts.index = ['Итого']

print(pivot_table)
print(total_ship_counts)