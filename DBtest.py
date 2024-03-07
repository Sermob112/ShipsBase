from PySide6.QtWidgets import *
from peewee import SqliteDatabase, Model, AutoField, CharField, IntegerField, FloatField, DateField
from playhouse.shortcuts import model_to_dict
from datetime import date
from PySide6.QtCore import *
from PySide6.QtGui import QColor
import sys, json
from PySide6.QtGui import QFont,QDesktopServices
from peewee import JOIN
from models import Ship
# from insertPanel import InsertWidgetPanel
# from insertPanelContract import InsertPanelContract

# from InsertWidgetNMCK import InsertWidgetNMCK
# from InsertWidgetCEIA import InsertWidgetCEIA
# from InsertWidgetCurrency import InsertWidgetCurrency
# from parserV3 import delete_records_by_id, export_to_excel
from datetime import datetime
from PySide6.QtWidgets import QSizePolicy
import os
import subprocess
from openpyxl import Workbook
from PySide6.QtCore import Signal
# Код вашей модели остается таким же, как вы предоставили в предыдущем сообщении.



# Создаем соединение с базой данных
db = SqliteDatabase('test.db')
cursor = db.cursor()



class PurchasesWidget(QWidget):
    closingSignal = Signal()
    def __init__(self,main_window,role, user):
        super().__init__()
        self.main_win = main_window
        self.selected_text = None
        self.role = role
        self.user = user
        # self.changer = changer
        # Создаем таблицу для отображения данных
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # Устанавливаем первой колонке режим изменения размера по содержимому
        self.table.horizontalHeader().setStretchLastSection(True) # Растягиваем вторую колонку на оставшееся пространство
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setColumnWidth(0, 500)
        self.table.setWordWrap(True) # Разрешаем перенос текста в ячейках
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.current_position =0
        self.BackButton = QPushButton("Назад", self)
        self.BackButton.clicked.connect(self.go_back)
        self.deleteButton = QPushButton("Удалить запись", self)
        self.deleteButton.setFixedWidth(200)
        self.deleteButton.clicked.connect(self.remove_button_clicked)
        self.addButtonContract = QPushButton("Добавить обоснование НМЦК", self)
        self.BackButton.hide()
        self.addButtonContract.setMaximumWidth(400)
        
        self.addButtonTKP = QPushButton("Добавить результаты закупки", self)
        self.addButtonTKP.setMaximumWidth(400)
        # self.addButtonCIA = QPushButton("Добавить ЦКЕИ", self)
        self.addButtonCurrency= QPushButton("Экспорт в Еxcel Формуляра Закупок", self)
        self.addButtonCurrency.setMaximumWidth(300)
        self.label_form = QLabel() 
        self.label_form.setText("Редактирование Формуляра")

         # Устанавливаем обработчики событий для кнопок
        self.addButtonContract.clicked.connect(self.add_button_nmck_clicked)
        self.addButtonTKP.clicked.connect(self.add_button_contract_clicked)
        # self.addButtonCIA.clicked.connect(self.add_button_cia_clicked)

        self.addButtonCurrency.clicked.connect(self.show_current_purchase_to_excel)
        
         # Создаем метку
        self.label = QLabel("", self)
        # Устанавливаем обработчики событий для кнопок


        button_layout = QHBoxLayout()
        vertical_labels = QVBoxLayout()
        vertical_labels.addWidget(self.label_form)
        self.butlayout = QHBoxLayout()
        vertical_labels.addLayout(self.butlayout)
        self.butlayout.addWidget(self.addButtonContract )
        self.butlayout.addWidget(self.addButtonTKP )
        self.butlayout.setAlignment(Qt.AlignLeft)
        button_layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignHCenter)
        # Создаем горизонтальный макет и добавляем элементы
        button_layout2 = QHBoxLayout()

        
        # button_layout2.addWidget(self.addButtonTKP)
        # button_layout2.addWidget(self.addButtonContract, alignment=Qt.AlignLeft)
        # button_layout2.addWidget(self.addButtonTKP,alignment=Qt.AlignLeft)
        # button_layout2.addWidget(self.addButtonCIA)
        # Создаем слой для центрирования
       # Создаем слой для центрирования
                
        # Добавляем первую кнопку
        button_layout2.addWidget(self.addButtonCurrency,alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addStretch()
        button_layout2.addWidget(self.deleteButton)
        # button_layout2.setAlignment(Qt.AlignCenter)
   

 
       # Создаем горизонтальный макет и добавляем элементы
        layout = QVBoxLayout(self)

        # Создаем горизонтальный макет для минимальной и максимальной цены
        self.table.itemClicked.connect(self.open_file)
        # Добавляем таблицу и остальные элементы в макет
        layout.addLayout( vertical_labels)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        layout.addLayout(button_layout2)
        
        # Получаем данные из базы данных и отображаем первую запись
        self.reload_data()
    
        # self.purchases = Purchase.select()
        # self.purchases = (Purchase
        #         .select()
        #         .join(Contract, JOIN.LEFT_OUTER)
        #           # Уточните условия, если нужно
        #         )
        # combined_list = (Purchase
        #         .select()
        #         .join(Contract, JOIN.LEFT_OUTER)
        #           # Уточните условия, если нужно
        #         .execute())
   
        # self.purchases_list = list(self.purchases)
        # self.purchases_list = list(self.purchases)
        # self.show_current_purchase()

        if self.role == "Гость":
            self.addButtonCurrency.hide()
        else:
            self.addButtonCurrency.show()

        if self.role == "Гость" or self.role == "Пользователь":
            self.addButtonContract.hide()
            self.deleteButton.hide()
        else:
            self.addButtonCurrency.show()
            self.deleteButton.show()
    def remove_button_clicked(self):
        # reply = QMessageBox.question(self, 'Подтверждение удаления', 'Вы точно хотите удалить выбранные записи?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if reply == QMessageBox.Yes:
        reply = QMessageBox()
        reply.setWindowTitle("Удаление")
        reply.setText('Вы точно хотите удалить текущую запись?')
        
        reply.addButton("Нет", QMessageBox.NoRole)
        reply.addButton("Да", QMessageBox.YesRole)
        result = reply.exec()
        if result == 1:
            if self.current_purchase.Id:
                success = delete_records_by_id([self.current_purchase.Id],user=self.user, role= self.role)
                if success:
                    self.main_win.updatePurchaseLabel()
                    
                    QMessageBox.information(self, "Успех", "Вы успешно удалили запись!")
                    self.reload_data()
                else:
                    QMessageBox.information(self,"Ошибка", "Ошибка при удалении записей")
                    
                  
        else:
            pass
    
    def closeEvent(self, event):
        self.closingSignal.emit()
        event.accept()
    def show_current_purchase(self):
     
        if len(self.purchases_list) != 0:
            current_ship = self.purchases_list[self.current_position]
            # Отображаем информацию о текущей записи в лейбле
            # self.label.setText(f"Запись {self.current_position + 1} из {len(self.purchases_list)}")
            # Дополнительный код для отображения записи в таблице (замените на свой код)
            # self.table.setItem(row, column, QTableWidgetItem(str(current_purchase.some_property)))
        else:
            self.label.setText("Нет записей")
        # Очищаем таблицу перед добавлением новых данных
        self.table.setRowCount(0)
        if len(self.purchases_list) != 0:
            # Получаем текущую запись
            self.current_purchase = self.purchases_list[self.current_position]

            # Добавляем данные в виде "название поля - значение поля"
            self.add_section_to_table("Описание судна")
            self.add_row_to_table("ID", str(current_ship.id))
            self.add_row_to_table("Регистрационный номер", current_ship.reg_number if current_ship.reg_number else "Нет данных")
            self.add_row_to_table("Название", current_ship.name if current_ship.name else "Нет данных")
            self.add_row_to_table("Заводской номер", current_ship.construction_number if current_ship.construction_number else "Нет данных")
            self.add_row_to_table("Проект судна", current_ship.ship_project if current_ship.ship_project else "Нет данных")
            self.add_row_to_table("Тип и назначение", current_ship.type_and_purpose if current_ship.type_and_purpose else "Нет данных")
            self.add_row_to_table("Дата постройки", str(current_ship.construction_date) if current_ship.construction_date else "Нет данных")
            self.add_row_to_table("Место постройки", current_ship.construction_place if current_ship.construction_place else "Нет данных")
            self.add_row_to_table("Категория по формуле", current_ship.class_formula_category if current_ship.class_formula_category else "Нет данных")
            self.add_row_to_table("Общая длина", str(current_ship.overall_length) if current_ship.overall_length else "Нет данных")
            self.add_row_to_table("Конструктивная длина", str(current_ship.constructive_length) if current_ship.constructive_length else "Нет данных")
            self.add_row_to_table("Общая ширина", str(current_ship.overall_width) if current_ship.overall_width else "Нет данных")
            self.add_row_to_table("Конструктивная ширина", str(current_ship.constructive_width) if current_ship.constructive_width else "Нет данных")
            self.add_row_to_table("Водоизмещение", str(current_ship.displacement) if current_ship.displacement else "Нет данных")
            self.add_row_to_table("Грузоподъемность", str(current_ship.deadweight) if current_ship.deadweight else "Нет данных")
            self.add_row_to_table("Вместимость груза", str(current_ship.cargo_capacity) if current_ship.cargo_capacity else "Нет данных")
            self.add_row_to_table("Поперечные шпонки", str(current_ship.transverse_bulkheads) if current_ship.transverse_bulkheads else "Нет данных")
            self.add_row_to_table("Продольные шпонки", str(current_ship.longitudinal_bulkheads) if current_ship.longitudinal_bulkheads else "Нет данных")
            self.add_row_to_table("Пассажирская вместимость", str(current_ship.passenger_capacity) if current_ship.passenger_capacity else "Нет данных")
            self.add_row_to_table("Экипаж", str(current_ship.crew) if current_ship.crew else "Нет данных")
            self.add_row_to_table("Группа организации", current_ship.organization_group if current_ship.organization_group else "Нет данных")
            self.add_row_to_table("Балластные баки", str(current_ship.ballast_tanks) if current_ship.ballast_tanks else "Нет данных")
            self.add_row_to_table("Общая емкость баков", str(current_ship.total_tank_capacity) if current_ship.total_tank_capacity else "Нет данных")
            self.add_row_to_table("Грузоподъемность крана 1", str(current_ship.crane_1_capacity) if current_ship.crane_1_capacity else "Нет данных")
            self.add_row_to_table("Грузоподъемность крана 2", str(current_ship.crane_2_capacity) if current_ship.crane_2_capacity else "Нет данных")
            self.add_row_to_table("Грузоподъемность крана 3", str(current_ship.crane_3_capacity) if current_ship.crane_3_capacity else "Нет данных")
            self.add_row_to_table("Материал корпуса", current_ship.hull_material if current_ship.hull_material else "Нет данных")
            self.add_row_to_table("Материал надстройки", current_ship.superstructure_material if current_ship.superstructure_material else "Нет данных")
            self.add_row_to_table("Тип основного двигателя", current_ship.main_engine_type if current_ship.main_engine_type else "Нет данных")
            self.add_row_to_table("Модель основного двигателя", current_ship.main_engine_model if current_ship.main_engine_model else "Нет данных")
            self.add_row_to_table("Мощность основного двигателя (кВт)", str(current_ship.main_engine_power_kw) if current_ship.main_engine_power_kw else "Нет данных")
            self.add_row_to_table("Количество основных двигателей", str(current_ship.main_engine_quantity) if current_ship.main_engine_quantity else "Нет данных")
            self.add_row_to_table("Общая мощность основных двигателей (кВт)", str(current_ship.total_engine_power_kw) if current_ship.total_engine_power_kw else "Нет данных")
            self.add_row_to_table("Общая мощность генераторов (кВт)", str(current_ship.total_generators_kw) if current_ship.total_generators_kw else "Нет данных")
            self.add_row_to_table("Общая мощность вспомогательных двигателей (кВт)", str(current_ship.total_auxiliary_engines_kw) if current_ship.total_auxiliary_engines_kw else "Нет данных")
            # Получаем связанные записи из модели Contract
          
            # if current_purchase.isChanged == True:
            #     self.currency = CurrencyRate.select().where(CurrencyRate.purchase == current_purchase)
            #     for curr in self.currency:
            #         self.add_section_to_table("Изминения валюты")
            #         self.add_row_to_table("Значение валюты", str(curr.CurrencyValue))
            #         self.add_row_to_table("Текущая валюта", str(curr.CurrentCurrency))
            #         self.add_row_to_table("Дата изменения значения валюты", str(curr.DateValueChanged))
            #         self.add_row_to_table("Дата курса валюты", str(curr.CurrencyRateDate))
            #         self.add_row_to_table("Предыдущая валюта", str(curr.PreviousCurrency))
        else:
            self.label.setText("Нет записи")

    def add_row_to_table(self, label_text, value_text):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        label_item = QTableWidgetItem()
        label_item.setText(label_text)
        label_item.setFlags(label_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        label_font = QFont()
        label_font.setPointSize(10)
        label_item.setFont(label_font)

        value_item = QTableWidgetItem()
        value_item.setText(value_text)
        value_item.setFlags(value_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        value_font = QFont()
        value_font.setPointSize(10)
        value_item.setFont(value_font)
        
        if label_text == "Файл НМЦК" or label_text == "Файл протокола" or label_text == "Извещение о закупке" or label_text == "Файл расчета" or label_text == "Файл итогового определения НМЦК с использованием нескольких методов" or label_text == "Договор":
            if value_text != "Нет данных":
                # Установка цвета фона только для нужных ячеек
                label_item.setBackground(QColor(200, 255, 200))  # Светло-зеленый
                value_item.setBackground(QColor(200, 255, 200))  # Светло-зеленый
        if label_text == 'Реестровый номер':
            value_item.setData(Qt.UserRole, f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={self.purchases_list[self.current_position].RegistryNumber}&morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1')
            value_item.setForeground(Qt.blue)  # Голубой цвет текста
        
        self.table.setItem(row_position, 0, label_item)
        self.table.setItem(row_position, 1, value_item)
        

        # # Adjust row height
        self.table.resizeRowsToContents()
        # max_height = 40  # Установите желаемую максимальную высоту здесь
        # self.table.setRowHeight(row_position, min(max_height, self.table.rowHeight(row_position)))

    
    def add_section_to_table(self, section_text):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        section_item = QTableWidgetItem(section_text)
        section_item.setFlags(section_item.flags() & ~Qt.ItemIsEditable)  # Заголовок не редактируемый
        # section_item.setBackground(QColor(200, 200, 200))  # Цвет фона заголовка
        section_item.setTextAlignment(Qt.AlignCenter)

        self.table.setItem(row_position, 0, section_item)
        self.table.setSpan(row_position, 0, 1, 2)  # Занимаем два столбца


    def add_button_nmck_clicked(self):
        
        if len(self.purchases_list) != 0:
            self.current_purchase = self.purchases_list[self.current_position]
            purchase_id = self.current_purchase.Id
     
            self.insert_cont = InsertWidgetPanel(purchase_id,self,self.role,self.user,self.changer)
            # self.insert_cont.setParent(self)
            self.closingSignal.connect(self.insert_cont.close)
            self.insert_cont.show()

    def add_button_contract_clicked(self):
        
        if len(self.purchases_list) != 0:
            self.current_purchase = self.purchases_list[self.current_position]
            purchase_id = self.current_purchase.Id
     
            self.insert_cont = InsertPanelContract(purchase_id,self,self.role,self.user,self.changer)
            # self.insert_cont.setParent(self)
            self.closingSignal.connect(self.insert_cont.close)
            self.insert_cont.show()
    
    def open_file(self, item):
        column = item.column()

      
        if column == 1:  # Проверяем, что кликнули по значению (колонка с путем к файлу)
            file_path = item.text()
            if os.path.isfile(file_path):
                # subprocess.Popen(['start', 'excel', file_path], shell=True)  # Открываем файл
                if file_path.lower().endswith(('.docx', '.doc')):
                    subprocess.Popen(['start', 'winword', file_path], shell=True)
                elif file_path.lower().endswith('.pdf'):
                    subprocess.Popen(['start', 'winword', file_path], shell=True)
                elif file_path.lower().endswith(('.xlsx', '.xls','.csv')):
                    subprocess.Popen(['start', 'excel', file_path], shell=True)
                    print('here3')
                else:
                    self.show_warning("Неизвестный формат файла", "Невозможно определить программу для открытия.")
            if "№" in item.text():
                print("Текст содержит символ '№'")
                url = item.data(Qt.UserRole)
                QDesktopServices.openUrl(QUrl(url))
            if "download" in item.text():
                url_for = item.text()
                QDesktopServices.openUrl(QUrl(url_for))

            else:
                pass
            #    self.show_warning("Неизвестный формат файла", "Невозможно определить программу для открытия.")


    def add_button_tkp_clicked(self):
        if len(self.purchases_list) != 0:
            self.current_purchase = self.purchases_list[self.current_position]
            purchase_id = self.current_purchase.Id
            self.tkp_shower = InsertWidgetNMCK(purchase_id,self)
            self.tkp_shower.show()
    
    def add_button_cia_clicked(self):
        if len(self.purchases_list) != 0:
            self.current_purchase = self.purchases_list[self.current_position]
            purchase_id = self.current_purchase.Id
            self.cia_shower = InsertWidgetCEIA(purchase_id,self)
            self.cia_shower.show()
    def go_back(self):
        if self.window:
            self.main_win.stackedWidget.setCurrentIndex(0)
     

    # def file_exit(self):
    #     if len(self.purchases_list) != 0:
    #         self.current_purchase = self.purchases_list[self.current_position]
    #         purchase_id = self.current_purchase.Id
    #         self.curr_shower = InsertWidgetCurrency(purchase_id)
    #         self.curr_shower.show()
    # def update_currency(self):
    #     if len(self.purchases_list) != 0:
    #         self.current_purchase = self.purchases_list[self.current_position]
    #         purchase_id = self.current_purchase.Id
    #         self.curr_shower = InsertWidgetCurrency(purchase_id)
    #         self.curr_shower.show()
    
        
    def reload_data(self):
        self.purchases = Ship.select()
        self.purchases_list = list(self.purchases)
        self.update()
        self.show_current_purchase()
        

    def reload_data_id(self,id):
        self.purchases = Ship.select().where(Ship.id == id)
        self.purchases_list = list(self.purchases)
        self.update()
        self.show_current_purchase()
        

    def show_warning(self, title, text):
        warning = QMessageBox.warning(self, title, text, QMessageBox.Ok)
    def show_current_purchase_to_excel(self):
        wb = Workbook()
        ws = wb.active
        
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is not None:
                item_text = item.text()
                if item_text.startswith("Описание закупки") or \
                item_text.startswith("Определение НМЦК и ЦКЕИ") or \
                item_text.startswith("Определение победителя") or \
                item_text.startswith("Заключение контракта") or \
                item_text.startswith("1.Определение НМЦК методом сопоставимых рыночных цен") or \
                item_text.startswith("2.Определение НМЦК методом сопоставимых рыночных цен (анализа рынка) при использовании общедоступной информании") or \
                item_text.startswith("3.Определение НМЦК затратным методом") or \
                item_text.startswith("4.Итоговое определение НМЦК с использованием нескольких методов"):
                    ws.append([item_text])  # Добавляем заголовок раздела
                else:
                    label_item = self.table.item(row, 0)
                    value_item = self.table.item(row, 1)
                    if label_item is not None and value_item is not None:
                        label_text = label_item.text()
                        value_text = value_item.text()
                        if label_text and value_text:  # Проверка на пустую строку
                            ws.append([label_text, value_text])
        
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        self.purchases = Purchase.select()
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            selected_file = selected_file if selected_file else None
            if selected_file:
                wb.save(f'{selected_file}\формуляр закупки {self.current_purchase.RegistryNumber}.xlsx')
                QMessageBox.warning(self, "Успех", "Файл успешно сохранен")
       

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     csv_loader_widget = PurchasesWidget()
#     csv_loader_widget.show()
#     sys.exit(app.exec())