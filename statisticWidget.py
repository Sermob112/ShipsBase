from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QStringListModel,Signal
from PySide6.QtGui import *
from peewee import *
import pandas as pd
from models import Ship
import json
from functools import partial

class StatisticWidget(QWidget):
    def __init__(self, all_purches,role):
        super().__init__()
        self.all_purchase = all_purches
        self.role = role
        self.init_ui()
        
    def init_ui(self):
        # Создаем лейбл
        self.label_text = "Статистический анализ методов, использованных для определения НМЦК и ЦКЕП"
        self.label = QLabel(self.label_text)
        self.label_filter_order = QLabel("Фильтры: ")
        self.label_filter_data = QLabel("Фильтры: ")
        self.label_filter_price = QLabel("Фильтры: ")
        self.label_filter_okpd2 = QLabel("Фильтры: ")
         # Создаем кнопки "Назад" и "Вперед"
        # btn_back = QPushButton("Назад", self)
        # btn_forward = QPushButton("Вперед", self)
        self.toExcel = QPushButton("Экспорт в Excel", self)
        self.Update = QPushButton("Обновить", self)
        self.Reset_filters = QPushButton("Сбросить фильтры", self)
        # btn_analysis = QPushButton("Анализ", self)
        self.query = self.all_purchase.return_filtered_purchase()
        # btn_back.clicked.connect(self.show_previous_data)
        # btn_forward.clicked.connect(self.show_next_data)
        self.toExcel.clicked.connect(self.export_to_excel_clicked)
        self.Update.clicked.connect(self.update_data)
        self.Reset_filters.clicked.connect(self.reset_filters)
        # Инициализация переменной для отслеживания текущего индекса данных
        self.current_data_index = 0

        # btn_analysis.clicked.connect(self.analisMAxPrice)
        # Создаем таблицу
        self.table = QTableWidget(self)
        
        # self.table.setColumnCount(4)
        # self.table.setHorizontalHeaderLabels(["Метод", "223-ФЗ"])

        # self.table.setColumnWidth(0, 300)  # Ширина "Метод"
        # self.table.setColumnWidth(1, 100)  # Ширина "223-ФЗ"
        # self.table.setColumnWidth(2, 100)  # Ширина "44-ФЗ"
        # Устанавливаем политику расширения таблицы
        # self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Установите политику изменения размеров секций горизонтального заголовка
        self.table.horizontalHeader().setStretchLastSection(True)
        # Установите политику изменения размеров колонок содержимого
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
          # Список для хранения всех данных, которые  отобразить в таблице
        # self.all_data = [self.analis(),self.analisNMSK(),self.analisOKPD2(),self.analisQueryCount(), 
        #                  self.analisQueryCountAccept(),self.analisQueryCountDecline(),
        #                  self.analisNMCKReduce(),self.analyze_price_count(), self.analisMAxPrice(),self.analisCoeffVar()]
        self.all_data = [self.analis()]
        
        self.label_texts = [
            "Анализ методов, использованных для определения НМЦК и ЦКЕП"
        ]
        self.buttons = []

        # Добавляем горизонтальную линию
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)  # Форма линии (горизонтальная)
        line.setFrameShadow(QFrame.Shadow.Sunken)  # Тень линии
        line.setStyleSheet("background-color: grey;")  # Цвет фона
        line.setFixedHeight(2)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        line1.setStyleSheet("background-color: grey;")
        line1.setFixedHeight(2)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        line2.setStyleSheet("background-color: grey;")
        line2.setFixedHeight(2)
         # Добавляем кнопку выпадающего меню Первый этап
        self.FirstStage = QPushButton("Анализ НМЦК")
        self.FirstStage.setIcon(QIcon("Pics/right-arrow.png"))
        self.FirstStage.setMaximumWidth(400)
        self.FirstStage.setStyleSheet("text-align: left; padding-left: 10px;font-size: 11pt;")
        self.FirstStage.clicked.connect(self.toggle_stage_1)
         # колапсирующее окно Первый этап
        self.menu_content = QWidget()
        menu_layout = QVBoxLayout()
        self.Qword = QLabel("Анализ методов и формулировок в государственных закупках")
        menu_layout.addWidget(self.Qword)
        for index, text in enumerate(self.label_texts[:3]):
           
            button = QtWidgets.QPushButton()
            button.setText(text) 
            button.setFixedSize(400,50)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            button.setSizePolicy(size_policy)
            button.setStyleSheet("text-align: left;padding-left: 8px;")
            button.clicked.connect(partial(self.show_specific_data, index, button))
            menu_layout.addWidget(button,alignment=Qt.AlignmentFlag.AlignTop)
            self.buttons.append(button)
        # menu_layout.addWidget(line)
        self.menu_content.setLayout(menu_layout)
        self.menu_frame = QFrame()
        self.menu_frame.setLayout(QVBoxLayout())
        self.menu_frame.layout().addWidget(self.menu_content)
        self.menu_frame.setVisible(False)

         # Добавляем кнопку выпадающего меню по цене
        self.SecondStage = QPushButton("Анализ Заявок")
        self.SecondStage.setIcon(QIcon("Pics/right-arrow.png"))
        self.SecondStage.setMaximumWidth(400)
        self.SecondStage.setStyleSheet("text-align: left;padding-left: 10px;font-size: 11pt;")
        self.SecondStage.clicked.connect(self.toggle_stage_2)
         # колапсирующее окно со списком всех элементов
        self.menu_content_2 = QWidget()
        menu_layout_2 = QVBoxLayout()
        self.Qword_2 = QLabel("Анализ заявок на участие в конкурсе")
        menu_layout_2.addWidget(self.Qword_2)
        for index , text in enumerate(self.label_texts[3:6]):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(400, 50)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            button.setSizePolicy(size_policy)
            button.setStyleSheet("text-align: left;padding-left: 8px;")
            button.clicked.connect(partial(self.show_specific_data, index + 3, button))
            menu_layout_2.addWidget(button,alignment=Qt.AlignmentFlag.AlignTop)
            self.buttons.append(button)
        # menu_layout_2.addWidget(line)
        self.menu_content_2.setLayout(menu_layout_2)
        self.menu_frame_2 = QFrame()
        self.menu_frame_2.setLayout(QVBoxLayout())
        self.menu_frame_2.layout().addWidget(self.menu_content_2)
        self.menu_frame_2.setVisible(False)

        # Добавляем кнопку выпадающего меню Первый этап
        self.ThirdStage = QPushButton("Анализ контрактов")
        self.ThirdStage.setIcon(QIcon("Pics/right-arrow.png"))
        self.ThirdStage.setMaximumWidth(400)
        self.ThirdStage.setStyleSheet("text-align: left;padding-left: 10px;font-size: 11pt;")
        self.ThirdStage.clicked.connect(self.toggle_stage_3)
         # колапсирующее окно Первый этап
        self.menu_content_3 = QWidget()
        menu_layout_3 = QVBoxLayout()
        self.Qword_3 = QLabel("Анализ заключенных контрактов и разницы НМЦК и ЦКЕИ")
        menu_layout_3.addWidget(self.Qword_3)
        for index, text in enumerate(self.label_texts[6:]):
            button = QtWidgets.QPushButton(text)
            button.setFixedSize(400, 50)
            
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            button.setSizePolicy(size_policy)
            button.setStyleSheet("text-align: left;padding-left: 8px;")
            button.clicked.connect(partial(self.show_specific_data, index + 6, button))
            menu_layout_3.addWidget(button,alignment=Qt.AlignmentFlag.AlignTop)
            self.buttons.append(button)
        # menu_layout.addWidget(line)
        self.menu_content_3.setLayout(menu_layout_3)
        self.menu_frame_3 = QFrame()
        self.menu_frame_3.setLayout(QVBoxLayout())
        self.menu_frame_3.layout().addWidget(self.menu_content_3)
        self.menu_frame_3.setVisible(False)
        
        #ЦИКЛ кнопок 
        # for index, text in enumerate(self.label_texts[:3]):
        #     button = QtWidgets.QPushButton(text)
        #     button.setFixedSize(800, 30)
        #     size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        #     button.setSizePolicy(size_policy)
        #     button.setStyleSheet("text-align: left;")
            
            
        #     # Подключите обработчик события к каждой кнопке, передавая индекс
        #     button.clicked.connect(partial(self.show_specific_data, index, button))
            
        #     self.buttons.append(button)
        
        self.buttons_layout = QVBoxLayout()

        # Добавьте кнопки в вертикальный слой
        # for button in self.buttons:
        #     self.buttons_layout.addWidget(button)

        main_layout = QHBoxLayout(self)
        # scroll_area = QScrollArea(self)
        # scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # scroll_widget = QtWidgets.QWidget()
        # scroll_widget.setLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.FirstStage)
        self.buttons_layout.addWidget(self.menu_frame)
        self.buttons_layout.addWidget(self.SecondStage)
        self.buttons_layout.addWidget(self.menu_frame_2)
        self.buttons_layout.addWidget(self.ThirdStage)
        self.buttons_layout.addWidget(self.menu_frame_3)
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # scroll_area.setWidget(scroll_widget)
        # main_layout.addWidget(scroll_area)
        main_layout.addLayout(self.buttons_layout)
        

        #  вертикальный слой для метки и таблицы
        self.vertical_layout = QVBoxLayout(self)
        self.filter_layout = QHBoxLayout(self)
        self.vertical_layout.addLayout(self.filter_layout)
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.table)

        # Добавьте вертикальный слой с меткой и таблицей в горизонтальный слой
        main_layout.addLayout(self.vertical_layout)

 #  вертикальный слой для кнопок внизу
        button_layout = QVBoxLayout(self)
        # button_layout.addWidget(btn_back)
        # button_layout.addWidget(btn_forward)

        #  вертикальный слой для кнопок внизу справа
        button_layout2_H = QHBoxLayout(self)
        button_layout2 = QVBoxLayout(self)
       
        button_layout2_H.addWidget(self.Update)
        button_layout2_H.addWidget(self.Reset_filters)
        button_layout2.addWidget(self.toExcel)
        button_layout2.addLayout(button_layout2_H)
        #  вертикальные слои с кнопками в горизонтальный слой
        self.vertical_layout.addLayout(button_layout)
        self.vertical_layout.addLayout(button_layout2)
        
        #  основной макет для вашего виджета
        self.setLayout(main_layout)
        #  отображение данных
        self.show_current_data()
        self.highlight_first_button()

        self.setLayout(main_layout)
        # self.analisQueryCount()
        # self.analisPriceCount()
        # self.analyze_price_count()
        if self.role == "Гость":
            self.toExcel.hide()
        else:
            self.toExcel.show()

    def toggle_stage_1(self):
        # Изменяем видимость содержимого при нажатии на кнопку
        self.menu_frame.setVisible(not self.menu_frame.isVisible())
        if self.menu_frame.isVisible():
            self.FirstStage.setIcon(QIcon("Pics/arrow-down.png"))
        else:
            self.FirstStage.setIcon(QIcon("Pics/right-arrow.png"))

    def toggle_stage_2(self):
        # Изменяем видимость содержимого при нажатии на кнопку
        self.menu_frame_2.setVisible(not self.menu_frame_2.isVisible())
        if self.menu_frame_2.isVisible():
            self.SecondStage.setIcon(QIcon("Pics/arrow-down.png"))
        else:
            self.SecondStage.setIcon(QIcon("Pics/right-arrow.png"))  
    def toggle_stage_3(self):
        # Изменяем видимость содержимого при нажатии на кнопку
        self.menu_frame_3.setVisible(not self.menu_frame_3.isVisible())
        if self.menu_frame_3.isVisible():
            self.ThirdStage.setIcon(QIcon("Pics/arrow-down.png"))
        else:
            self.ThirdStage.setIcon(QIcon("Pics/right-arrow.png")) 
    def update_data(self):
        # self.all_data = [self.analis(),self.analisNMSK(), self.analisMAxPrice(),self.analisCoeffVar(),self.analisQueryCount(), 
        #                  self.analisQueryCountAccept(),self.analisQueryCountDecline(),
        #                  self.analisNMCKReduce(),self.analyze_price_count(),self.analisOKPD2()]
        self.all_data = [self.analis()]
        self.show_current_data()
        self.query = self.all_purchase.return_filtered_purchase()
        sort_by_putch_order, min_date, max_date, min_price, max_price, okpd2= self.all_purchase.return_filters_variabels()
        self.filter_layout.addWidget(self.label_filter_data)
        self.filter_layout.addWidget(self.label_filter_order)
        self.filter_layout.addWidget(self.label_filter_price)
        self.filter_layout.addWidget(self.label_filter_okpd2)
        self.label_filter_data.setText(f"Фильтр по дате: с {min_date} по {max_date}")
        self.label_filter_order.setText(f"Фильтр по закону:{sort_by_putch_order}")
        self.label_filter_price.setText(f"Фильтр по цене:{min_price} - {max_price}")
        self.label_filter_okpd2.setText(f"Фильтр по ОКПД2:{okpd2}")
    def analyze_price_count(self):
        coeff_range_order = [
            'Ценовое предложение №1',
            'Ценовое предложение №2',
            'Ценовое предложение №3',
            'Ценовое предложение №4',
            'Ценовое предложение №5',
            'Ценовое предложение №6',
        ]

        query = Purchase.select(Purchase.PurchaseOrder, Contract.PriceProposal).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase)).where(Contract.PriceProposal.is_null(False))
        data = list(query)
        df_data = []

        for purchase in data:
            try:
                price_proposal_dict = json.loads(purchase.contract.PriceProposal)
            except json.JSONDecodeError:
                continue  # Пропустить запись, если JSON не может быть разобран

            row_data = [purchase.PurchaseOrder]
            for key in coeff_range_order:
                value = price_proposal_dict.get(key, "")
                row_data.append(self.count_non_empty_values({key: value}))

            df_data.append(row_data)

        df_columns = ['PurchaseOrder'] + coeff_range_order
        df = pd.DataFrame(df_data, columns=df_columns)

        # Создание сводной таблицы
        pivot_table = df.pivot_table(index='PurchaseOrder', aggfunc='sum', fill_value=0)
        # Суммы по строкам и столбцам
        transposed_table = pivot_table.T
        row_totals = transposed_table.sum(axis=1)
        transposed_table['Общий итог'] = row_totals
        column_sums = transposed_table.sum()
        total_counts = column_sums.sum()
        column_sums['Суммы'] = total_counts

        return transposed_table,column_sums
    def count_non_empty_values(self, dictionary):
        count = 0
        for key, value in dictionary.items():
            if value != "Нет данных" :
                count += 1
        return count
    def reset_filters(self):
        self.all_purchase.resetFilters()
        self.update_data()
    # def analisPriceCount(self):
    #     #Статистический анализ методов, использованных для определения НМЦК и ЦКЕП
    #     query = Purchase.select(Purchase.PurchaseOrder, Contract.PriceProposal).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase))
    #     t = list(query)
    #     # print(len(t))
    #     price_proposals_dict = {}
    #     i = 0
    #     for purchase in t:  # Используйте t, а не query
            
    #         # Извлекаем данные из результата запроса
    #         price_proposal = purchase.contract.PriceProposal

    #         # Парсим значение PriceProposal (пример, предполагая, что это JSON-строка)
    #         price_proposal_dict = json.loads(price_proposal)

    #         # Добавляем данные в общий словарь
    #         price_proposals_dict[i] = price_proposal_dict
    #         i = i + 1
       
       
    #     coeff_range_order = [
    #     'по 1-му предложению поставщиков',
    #     'по 2-м предложениям поставщиков',
    #     'по 3-м предложениям поставщиков',
    #     'по 4-м предложениям поставщиков',
    #     'по 5-ти предложениям поставщиков',
    #     'по 6-ти предложениям поставщиков',

    # ]
    #     # Создаем DataFrame
    #     query = Purchase.select(Purchase.PurchaseOrder, Contract.PriceProposal).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase))
    #     t = list(query)
    #     df = pd.DataFrame([(purchase.PurchaseOrder, purchase.contract.PriceProposal) for purchase in t], columns=['PurchaseOrder', 'PriceProposal'])
    #     # df['PriceProposal'] = df.apply(self.determine_price_range, axis=1)
    #     df['PriceProposal'] = pd.Categorical(df['PriceProposal'], categories=coeff_range_order, ordered=True)
    #     df = df.sort_values('PriceProposal')
    #     pivot_table = df.pivot_table(index='PriceProposal', columns='PurchaseOrder', aggfunc='size', fill_value=0)
    #     column_sums = pivot_table.sum()
    #     row_totals = pivot_table.sum(axis=1)
    #     pivot_table['Общий итог'] = row_totals
    #     column_sums2 = pivot_table.sum()
    #     column_means2 = pivot_table.mean()
    #     total_purchase_counts2 = column_sums2.sum()
    #     column_sums2['Суммы'] = total_purchase_counts2
    #     print(pivot_table)

    
    #     # print(pivot_table)
    #     return pivot_table
    

  
      
      
    def analis(self):
   
        ships = Ship.select()  # Предположим, что здесь вы делаете запрос к вашей модели Ship
        df = pd.DataFrame([(ship.construction_date.year, ship.id) for ship in ships], columns=['Год', 'Ед'])
        pivot_table = df.pivot_table(index='Год', aggfunc='size', fill_value=0)
        pivot_table.columns = ['Год', 'Ед']
        total_ship_counts = pivot_table.sum()

        total_purchase_counts = total_ship_counts.sum()
        # Создаем DataFrame из суммы
        total_ship_counts = pd.DataFrame({'Суммы': [total_purchase_counts]})
        total_ship_counts.index = ['Итого']
        pivot_table = pivot_table.reset_index()
        return pivot_table, total_ship_counts 
    
    
    def analisNMSK(self):
        #Статистический анализ методов, использованных для определения НМЦК и ЦКЕП
        purchases = self.query
        df = pd.DataFrame([(purchase.AuctionSubject, purchase.PurchaseOrder) for purchase in purchases], columns=['AuctionSubject', 'PurchaseOrder'])
        pivot_table = df.pivot_table(index='AuctionSubject', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        total_purchase_counts = column_sums.sum()
        column_sums['Суммы'] = total_purchase_counts
        return pivot_table, column_sums
    
    def analisOKPD2(self):
        # Получаем отфильтрованные данные из peewee
        purchases = self.query

        # Создаем DataFrame из отфильтрованных данных
        df = pd.DataFrame([(purchase.OKPD2Classification, purchase.PurchaseOrder) for purchase in purchases], columns=['OKPD2Classification', 'PurchaseOrder'])
        
        # Выполняем сводную таблицу
        pivot_table = df.pivot_table(index='OKPD2Classification', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        
        # Вычисляем суммы строк и столбцов
        column_sums = pivot_table.sum()
        row_totals = pivot_table.sum(axis=1)
        
        # Добавляем общий итог и суммы к сводной таблице
        pivot_table['Общий итог'] = row_totals
        column_sums['Суммы'] = column_sums.sum()

        return pivot_table, column_sums
      

    def analisMAxPrice(self):
        purchases = self.query.where(Purchase.InitialMaxContractPrice.is_null(False))
        price_range_order = [
            'Цена контракта более 100 000 000 тыс.руб.',
            'Цена контракта 5 000 000 - 10 000 000 тыс.руб.',
            'Цена контракта 1 000 000 - 5 000 000 тыс.руб.',
            'Цена контракта 500 000-  1 000 000 тыс.руб.',
            'Цена контракта 200 000 - 500 000 тыс.руб.',
            'Цена контракта 100 000 - 200 000 тыс.руб.',
            'Менее 100 тыс.руб'
          
        ]
        # Создаем DataFrame
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.InitialMaxContractPrice) for purchase in purchases],
                        columns=['PurchaseOrder', 'InitialMaxContractPrice'])
        df['PriceRange'] = df.apply(self.determine_price_range, axis=1)
        df['PriceRange'] = pd.Categorical(df['PriceRange'], categories=price_range_order, ordered=True)
        df = df.sort_values('PriceRange')
        pivot_table = df.pivot_table(index='PriceRange', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        column_sums2 = pivot_table.sum()
        column_means2 = pivot_table.mean()
        total_purchase_counts2 = column_sums2.sum()
        column_sums2['Суммы'] = total_purchase_counts2
     
        # Определите порядок категорий
       

        return pivot_table, column_sums2 
    def analisCoeffVar(self):
        purchases = self.query.where(Purchase.CoefficientOfVariation.is_null(False))
        coeff_range_order = [
        'Значение коэффициента вариации 0%',
        'значение коэффициента вариации 0-1%',
        'значение коэффициента вариации 1-2%',
        'значение коэффициента вариации 2-5%',
        'значение коэффициента вариации 5-10%',
        'значение коэффициента вариации 10-20%',
        'значение коэффициента вариации 20-33%',
        'более 33%'
    ]
        # Создаем DataFrame
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.CoefficientOfVariation) for purchase in purchases],
                        columns=['PurchaseOrder', 'CoefficientOfVariation'])
        df['CoeffRange'] = df.apply(self.determine_var_range, axis=1)
        df['CoeffRange'] = pd.Categorical(df['CoeffRange'], categories=coeff_range_order, ordered=True)
        df = df.sort_values('CoeffRange')
        pivot_table = df.pivot_table(index='CoeffRange', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        column_sums2 = pivot_table.sum()
        column_means2 = pivot_table.mean()
        total_purchase_counts2 = column_sums2.sum()
        column_sums2['Суммы'] = total_purchase_counts2
        return pivot_table, column_sums2 
    
    def analisNMCKReduce(self):
       
        coeff_range_order = [
        'Цена контракта совпадает с НМЦК и ЦКЕП',
        'Цена контракта ниже НМЦК и ЦКЕП на 0-1%',
        'Цена контракта ниже НМЦК и ЦКЕП на 1-5%',
        'Цена контракта ниже НМЦК и ЦКЕП на 5-10%',
        'Цена контракта ниже НМЦК и ЦКЕП на 10-20%',
        'Цена контракта ниже НМЦК и ЦКЕП более 20%',

    ]
        # Создаем DataFrame
        query = self.query.select(Purchase.PurchaseOrder, Contract.ReductionNMC).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase)).where(Contract.ReductionNMC.is_null(False))
        t = list(query)
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.contract.ReductionNMC) for purchase in t], columns=['PurchaseOrder', 'ReductionNMC'])
        df['ReductionNMC'] = df.apply(self.determine_NMCK_range, axis=1)
        df['ReductionNMC'] = pd.Categorical(df['ReductionNMC'], categories=coeff_range_order, ordered=True)
        df = df.sort_values('ReductionNMC')
        pivot_table = df.pivot_table(index='ReductionNMC', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        column_sums2 = pivot_table.sum()
        column_means2 = pivot_table.mean()
        total_purchase_counts2 = column_sums2.sum()
        column_sums2['Суммы'] = total_purchase_counts2
        return pivot_table, column_sums2
    
    def analisQueryCount(self):
        query = self.query.select(Purchase.PurchaseOrder, Contract.TotalApplications).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase)).where(Contract.TotalApplications.is_null(False))
        t = list(query)
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.contract.TotalApplications) for purchase in t], columns=['PurchaseOrder', 'TotalApplications'])
        pivot_table = df.pivot_table(index='TotalApplications', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        total_purchase_counts = column_sums.sum()
        column_sums['Суммы'] = total_purchase_counts
        # print(pivot_table)
        return pivot_table, column_sums

    def analisQueryCountAccept(self):
        query = self.query.select(Purchase.PurchaseOrder, Contract.AdmittedApplications).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase)).where(Contract.AdmittedApplications.is_null(False))
        t = list(query)
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.contract.AdmittedApplications) for purchase in t], columns=['PurchaseOrder', 'AdmittedApplications'])
        pivot_table = df.pivot_table(index='AdmittedApplications', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        total_purchase_counts = column_sums.sum()
        column_sums['Суммы'] = total_purchase_counts
        # print(pivot_table)
        return pivot_table, column_sums

    def analisQueryCountDecline(self):
        query = self.query.select(Purchase.PurchaseOrder, Contract.RejectedApplications).join(Contract, JOIN.LEFT_OUTER, on=(Purchase.Id == Contract.purchase)).where(Contract.RejectedApplications.is_null(False))
        t = list(query)
        df = pd.DataFrame([(purchase.PurchaseOrder, purchase.contract.RejectedApplications) for purchase in t], columns=['PurchaseOrder', 'RejectedApplications'])
        pivot_table = df.pivot_table(index='RejectedApplications', columns='PurchaseOrder', aggfunc='size', fill_value=0)
        column_sums = pivot_table.sum()
        
        row_totals = pivot_table.sum(axis=1)
        pivot_table['Общий итог'] = row_totals
        total_purchase_counts = column_sums.sum()
        column_sums['Суммы'] = total_purchase_counts
        # print(pivot_table)
        return pivot_table, column_sums




    # def save_to_excel(self, pivot_table, column_sums, output_excel_path):
    #     excel_df = pd.DataFrame(columns=['Методы закупок'] + list(pivot_table.columns) + ['Суммы'])

    #     for method, row in pivot_table.iterrows():
    #         excel_df = pd.concat([excel_df, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df.columns)])

    #     excel_df = pd.concat([excel_df, pd.DataFrame([['Суммы'] + list(column_sums) + [column_sums['Суммы']]], columns=excel_df.columns)])

    #     data_to_export = {'Методы закупок': excel_df}

    #     with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
    #         for sheet_name, df in data_to_export.items():
    #             df.to_excel(writer, sheet_name=sheet_name, index=False)

    # def save_to_excel_max_price(self, pivot_table, column_sums, output_excel_path):
    #     excel_df = pd.DataFrame(columns=['Уровень цены контракта'] + list(pivot_table.columns) + ['Суммы'])

    #     for method, row in pivot_table.iterrows():
    #         excel_df = pd.concat([excel_df, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df.columns)])

    #     # Ensure that the number of columns matches
    #     column_sums_row = ['Суммы'] + list(column_sums) + [column_sums['Суммы']]
    #     if len(column_sums_row) == len(excel_df.columns):
    #         excel_df = pd.concat([excel_df, pd.DataFrame([column_sums_row], columns=excel_df.columns)])

    #     data_to_export = {'Уровень цены контракта': excel_df}

    #     with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
    #         for sheet_name, df in data_to_export.items():
    #             df.to_excel(writer, sheet_name=sheet_name, index=False)

    # def save_to_excel_combined(self, pivot_table_purchase, column_sums_purchase, pivot_table_max_price, column_sums_max_price, output_excel_path):
    #     excel_df_purchase = pd.DataFrame(columns=['Методы закупок'] + list(pivot_table_purchase.columns) + ['Суммы'])

    #     for method, row in pivot_table_purchase.iterrows():
    #         excel_df_purchase = pd.concat([excel_df_purchase, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df_purchase.columns)])

    #     excel_df_purchase = pd.concat([excel_df_purchase, pd.DataFrame([['Суммы'] + list(column_sums_purchase) + [column_sums_purchase['Суммы']]], columns=excel_df_purchase.columns)])

    #     excel_df_max_price = pd.DataFrame(columns=['Уровень цены контракта'] + list(pivot_table_max_price.columns) + ['Суммы'])

    #     for method, row in pivot_table_max_price.iterrows():
    #         excel_df_max_price = pd.concat([excel_df_max_price, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df_max_price.columns)])

    #     column_sums_max_price_row = ['Суммы'] + list(column_sums_max_price) + [column_sums_max_price['Суммы']]
    #     if len(column_sums_max_price_row) == len(excel_df_max_price.columns):
    #         excel_df_max_price = pd.concat([excel_df_max_price, pd.DataFrame([column_sums_max_price_row], columns=excel_df_max_price.columns)])

    #     data_to_export = {'Методы закупок': excel_df_purchase, 'Уровень цены контракта': excel_df_max_price}

    #     with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
    #         for sheet_name, df in data_to_export.items():
    #             df.to_excel(writer, sheet_name=sheet_name, index=False)
    def save_to_excel_combined(self, pivot_tables_purchase, column_sums_purchase, pivot_tables_max_price, column_sums_max_price, output_excel_path):
        data_to_export = {}

        for idx, (pivot_table_purchase, column_sum_purchase) in enumerate(zip(pivot_tables_purchase, column_sums_purchase)):
            excel_df_purchase = pd.DataFrame(columns=['Метод'] + list(pivot_table_purchase.columns) + ['Суммы'])

            for method, row in pivot_table_purchase.iterrows():
                excel_df_purchase = pd.concat([excel_df_purchase, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df_purchase.columns)])

            column_sums_purchase_row = ['Суммы'] + list(column_sum_purchase) + [column_sum_purchase['Суммы']]
            if len(column_sums_purchase_row) == len(excel_df_purchase.columns):
                excel_df_purchase = pd.concat([excel_df_purchase, pd.DataFrame([column_sums_purchase_row], columns=excel_df_purchase.columns)])

            data_to_export[self.label_texts[idx][:20]] =excel_df_purchase

        for idx, (pivot_table_max_price, column_sum_max_price) in enumerate(zip(pivot_tables_max_price, column_sums_max_price)):
            excel_df_max_price = pd.DataFrame(columns=['Метод'] + list(pivot_table_max_price.columns) + ['Суммы'])

            for method, row in pivot_table_max_price.iterrows():
                excel_df_max_price = pd.concat([excel_df_max_price, pd.DataFrame([[method] + list(row) + [row.sum()]], columns=excel_df_max_price.columns)])

            column_sums_max_price_row = ['Суммы'] + list(column_sum_max_price) + [column_sum_max_price['Суммы']]
            if len(column_sums_max_price_row) == len(excel_df_max_price.columns):
                excel_df_max_price = pd.concat([excel_df_max_price, pd.DataFrame([column_sums_max_price_row], columns=excel_df_max_price.columns)])
            
            
            data_to_export[self.label_texts[idx + 5][:20]] = excel_df_max_price
            # data_to_export[f'Метод_{idx}'] = excel_df_max_price


        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            selected_file = selected_file if selected_file else None
            if selected_file:
                with pd.ExcelWriter(f'{selected_file}/{output_excel_path}', engine='openpyxl') as writer:
                    for sheet_name, df in data_to_export.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                QMessageBox.warning(self, "Успех", "Файл успешно сохранен")
                
            else:
                QMessageBox.warning(self, "Предупреждение", "Не выбран файл для сохранения")

        # with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        #     for sheet_name, df in data_to_export.items():
        #         df.to_excel(writer, sheet_name=sheet_name, index=False)
    def clear_table(self):
        self.table.setRowCount(0)




    def populate_table(self, data, sums):
    # Очищаем таблицу перед обновлением
        self.clear_table()

        # Получаем список всех уникальных законов
        all_purchase_orders = set(data.columns.tolist())
        # all_purchase_orders.remove('Общий итог')

        # Устанавливаем количество столбцов в таблице
        num_columns = len(all_purchase_orders) # Плюс два для "Метод" и "Общий итог"
        self.table.setColumnCount(num_columns)
        
        # Устанавливаем заголовки столбцов
        header_labels = list(all_purchase_orders)
        self.table.setHorizontalHeaderLabels(header_labels)

        # Добавляем строки в таблицу
        for index, row in data.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Заполняем ячейки в строке
            self.table.setItem(row_position, 0, QTableWidgetItem(index))  # Метод
            for col_index, purchase_order in enumerate(all_purchase_orders):
                value = row.get(purchase_order, 0)  # Получаем значение из DataFrame, если оно есть, иначе 0
                self.table.setItem(row_position, col_index , QTableWidgetItem(str(value)))
        # for row_index, row_sum in enumerate(data['Общий итог']):
        #     item = QTableWidgetItem(str(row_sum))
        #     self.table.setItem(row_index, self.table.columnCount() - 1, item)

      
        # # Добавляем строку с суммами
        # row_position = self.table.rowCount()
        # self.table.insertRow(row_position)
        # self.table.setItem(row_position, 0, QTableWidgetItem('Суммы'))

        # for col_index, key in enumerate(sums.keys()):
        #     value = sums[key]
        #     self.table.setItem(row_position, col_index + 1, QTableWidgetItem(str(value)))
      
    



    def determine_NMCK_range(self,row):
        try:
            if row['ReductionNMC'] * 100 == 0:
                return 'Цена контракта совпадает с НМЦК и ЦКЕП'
            elif 0 <= row['ReductionNMC'] * 100 <= 1:
                return 'Цена контракта ниже НМЦК и ЦКЕП на 0-1%'
            elif 1 <= row['ReductionNMC'] * 100 <= 5:
                return 'Цена контракта ниже НМЦК и ЦКЕП на 1-5%'
            elif 5 <= row['ReductionNMC'] * 100<= 10:
                return 'Цена контракта ниже НМЦК и ЦКЕП на 5-10%'
            elif 10 <= row['ReductionNMC'] * 100 <= 20:
                return 'Цена контракта ниже НМЦК и ЦКЕП на 10-20%'
            else:
                return 'Цена контракта ниже НМЦК и ЦКЕП более 20%'
        except:
            pass
        
    def determine_var_range(self,row):
        try:
            if row['CoefficientOfVariation'] * 100 == 0:
                return 'Значение коэффициента вариации 0%'
            elif 0 <= row['CoefficientOfVariation'] * 100 <= 1:
                return 'значение коэффициента вариации 0-1%'
            elif 1 <= row['CoefficientOfVariation'] * 100 <= 2:
                return 'значение коэффициента вариации 1-2%'
            elif 2 <= row['CoefficientOfVariation'] * 100<= 5:
                return 'значение коэффициента вариации 2-5%'
            elif 5 <= row['CoefficientOfVariation'] * 100<= 10:
                return 'значение коэффициента вариации 5-10%'
            elif 10 <= row['CoefficientOfVariation']* 100 <= 20:
                return 'значение коэффициента вариации 10-20%'
            elif 20 <= row['CoefficientOfVariation']* 100 <= 33:
                return 'значение коэффициента вариации 10-20%'
            else:
                return 'более 33%'
        except:
            pass
        
    def determine_price_range(self,row):
        if row['InitialMaxContractPrice'] > 100000000:
            return 'Цена контракта более 100 000 000 тыс.руб.'
        elif 5000000 <= row['InitialMaxContractPrice'] <= 10000000:
            return 'Цена контракта 5 000 000 - 10 000 000 тыс.руб.'
        elif 1000000 <= row['InitialMaxContractPrice'] <= 5000000:
            return 'Цена контракта 1 000 000 - 5 000 000 тыс.руб.'
        elif 500000 <= row['InitialMaxContractPrice'] <= 1000000:
            return 'Цена контракта 500 000-  1 000 000 тыс.руб.'
        elif 200000 <= row['InitialMaxContractPrice'] <= 500000:
            return 'Цена контракта 200 000 - 500 000 тыс.руб.'
        elif 100000 <= row['InitialMaxContractPrice'] <= 200000:
            return 'Цена контракта 100 000 - 200 000 тыс.руб.'
        # elif 100000 <= row['InitialMaxContractPrice']:
        #     return 'Менее 100 тыс.руб'
        else:
            return 'Менее 100 тыс.руб'
        
    def show_current_data(self):
        # Очистка таблицы перед обновлением
        self.clear_table()

        # Получение текущих данных
        current_data = self.all_data[self.current_data_index]

        # Отображение данных в таблице
        self.populate_table(current_data[0], current_data[1])

    def show_previous_data(self):
        # Уменьшаем индекс данных, если это возможно
        if self.current_data_index > 0:
            self.current_data_index -= 1
            self.show_current_data()
            self.label.setText(self.label_texts[self.current_data_index])

    def show_next_data(self):
        # Увеличиваем индекс данных, если это возможно
        if self.current_data_index < len(self.all_data) - 1:
            self.current_data_index += 1
            self.show_current_data()
            self.label.setText(self.label_texts[self.current_data_index])

    def export_to_excel_clicked(self ):
        pivot_tables_purchase1, column_sums_purchase1 = self.analisQueryCountDecline()
        pivot_tables_purchase2, column_sums_purchase2 = self.analisNMSK()
        pivot_tables_purchase3, column_sums_purchase3 = self.analisQueryCount()
        pivot_tables_purchase4, column_sums_purchase4 = self.analisQueryCountAccept()
        pivot_tables_purchase5, column_sums_purchase5 = self.analisQueryCountDecline()
        pivot_tables_max_price1, column_sums_max_price1 = self.analisMAxPrice()
        pivot_tables_max_price2, column_sums_max_price2 = self.analisNMCKReduce()
        pivot_tables_max_price3, column_sums_max_price3 = self.analisCoeffVar()
        pivot_tables_max_price4, column_sums_max_price4= self.analyze_price_count()
        pivot_tables_max_price5, column_sums_max_price5= self.analisOKPD2()
        sort_by_putch_order, min_date, max_date, min_price, max_price, okpd2 = self.all_purchase.return_filters_variabels()
        filters = []

# Проверяем каждый фильтр на пустоту и добавляем непустые значения в список filters
        okpd2 = okpd2.replace(".", "_")
        okpd2 = okpd2.replace(":", "_")
        if sort_by_putch_order:
            filters.append(" " + sort_by_putch_order)
        if okpd2:
            filters.append(str(okpd2))
        if min_date:
            filters.append(" " + str(min_date))  # Преобразуем datetime.date в строку
        if max_date:
            filters.append(str(max_date))
        if min_price:
            filters.append(" " + str(min_price))
        if max_price:
            filters.append(str(max_price))
        
       
        file_name = f"Данные статистики по Фильтрам {' '.join(filters)}.xlsx"
        self.save_to_excel_combined(
        [pivot_tables_purchase1, pivot_tables_purchase2, pivot_tables_purchase3, pivot_tables_purchase4, pivot_tables_purchase5],
        [column_sums_purchase1, column_sums_purchase2, column_sums_purchase3, column_sums_purchase4, column_sums_purchase5],
        [pivot_tables_max_price1, pivot_tables_max_price2, pivot_tables_max_price3, pivot_tables_max_price4,pivot_tables_max_price5],
        [column_sums_max_price1, column_sums_max_price2, column_sums_max_price3, column_sums_max_price4,column_sums_max_price5],
        file_name
    )
    def show_specific_data(self, index, button):
    # Проверка, что индекс находится в пределах допустимых значений
        for btn in self.buttons:
            btn.setStyleSheet("text-align: left;")

        # Подсвечиваем только нажатую кнопку
        button.setStyleSheet("text-align: left; background-color: lightGreen;")

        # Обновляем текущую активную кнопку
        self.active_button = button
        if 0 <= index < len(self.label_texts):
            # Устанавливаем текущий индекс
            self.current_data_index = index
            self.show_current_data()
            self.label.setText(self.label_texts[self.current_data_index])
    def highlight_first_button(self):
    # Вызываем метод для подсветки первой кнопки
        if self.buttons:
            first_button = self.buttons[0]
            self.show_specific_data(0, first_button)
# if __name__ == "__main__":
#     from PySide6.QtWidgets import QApplication
#     import sys

#     app = QApplication(sys.argv)
#     window = StatisticWidget()
#     window.show()
#     sys.exit(app.exec())