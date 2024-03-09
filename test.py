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
df = pd.DataFrame([(ship.id, ship.construction_date.year) for ship in ships], columns=['Ед', 'Год'])
pivot_table = df.pivot_table(index='Год', aggfunc='size', fill_value=0)
pivot_table.columns = ['Ед', 'Год']
total_ship_counts = pivot_table.sum()

total_purchase_counts = total_ship_counts.sum()
# Создаем DataFrame из суммы
total_ship_counts = pd.DataFrame({'Суммы': [total_purchase_counts]})
total_ship_counts.index = ['Итого']


print(pivot_table)
print(total_ship_counts)