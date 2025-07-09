"""
Реализовать систему, описывающую работу склада товаров.
Два основных Класса:

Hub (синглтон, класс объекта нашего склада)
Item (класс предметов, хранящихся на складе)
Hub должен поддерживать обращение к предметам по индексам и иметь метод добавления предмета в лист _items, 
поле _date с датой в любом формате, а так же быть синглтоном (при любом вызове Hub() возвращается один и 
тот же инстантс объекта)
Item должен иметь уникальный _id, наиминование, описание, дату, в которую он должен быть отправлен а так же 
множество тегов _tags. Должен поддерживать добавление и удаление тегов. (В нашей задаче теги это просто строки 
ненулевой длинны, например "Хрупкий", "Скоропортящийся" и т.д.)
Hub:
атрибуты items, date, hub
методы add_item, rm_item

Items
атрибуты id(уникальный), name, description, dispatch_time, tags
методы add_tag, rm_tag
"""
import sys
import os
import unittest

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from src.hub import Hub, Item
from hub import Hub, Item

#1 Пользуясь полученными классами заведите hub, очистите его
hub1 = Hub()
hub1.clear()

print(f"\n1. Текущее состояние объекта hub1\n{hub1}\n", sep='')

#2 Добавьте в него несколько объектов
item_for_add = Item(
	    item_name='Armchair_',
	    description='africa',
	    dispatch_time='2021-03-02',
	    tags='',
	    cost=50*2
	)
hub1.add_item(item_for_add)

for i in range(5):
	item_for_add = Item(
	    item_name='fruit_' + str(i),
	    description='africa',
	    dispatch_time='2021-03-02',
	    tags=str(i),
	    cost=50*i
	)
	hub1.add_item(item_for_add)

for i in range(15):
	item_for_add = Item(
	    item_name='fruit_1' + str(i),
	    description='africa',
	    dispatch_time='2021-05-02',
	    tags=str(i),
	    cost=50*i
	)
	hub1.add_item(item_for_add)

item_for_add = Item(
	    item_name='apple_' + str(i),
	    description='africa',
	    dispatch_time='2021-03-02',
	    tags=str(i),
	    cost=50*i
	)
hub1.add_item(item_for_add)

print(f"\n2. В hub1 добавлены объекты Item\n", sep='')
for i in range(len(hub1)):
	print(hub1.get_item(i))

#3 Выбросите все объекты с названиями начинающиеся на "a" или "A", записав их в отдельный лист A
A = [hub1.get_item(i) for i in range(len(hub1)) if str(hub1.get_item(i))[:1] in ('A', 'a')]
hub1.drop_items(A)

print(f"\n3. Все объекты с именем на 'А' и 'а' перемещены из hub1 в А\nhub1:", sep='')
for i in range(len(hub1)):
	print(hub1.get_item(i))
print("\nA:", sep='')
for item in A:
	print(item)

#4 Выбросите все объекты с датой отправки раньше чем дата в hub, записав их в отдельный лист 
#  Outdated
Outdated = hub1.find_by_date('2021-04-03')
hub1.drop_items(Outdated)

print(f"\n4. Все объекты с датой раньше 2021-04-03 перемещены из hub1 в Outdated\nhub1:", sep='')
for i in range(len(hub1)):
	print(hub1.get_item(i))
print("\nOutdated:", sep='')
for item in Outdated:
	print(item)

#5 Выбросите топ-10 объектов из hub, записав их в MostValuable
#  Оставшиеся на складе объекты запишите в Others	
MostValuable = hub1.find_most_valuable(10)
hub1.drop_items(MostValuable)
Others = [hub1.get_item(i) for i in range(len(hub1))]

print(f"""\n5. Топ 10 объектов по стоимости перемещены из hub1 в MostValuable.
Оставшиеся объекты перемещены в Others.""", sep='')
print('\nMostValuable:', sep='')
for item in MostValuable:
	print("%-10s %8d" % (item, item.get_cost()))

print('\nOthers:', sep='')
for item in Others:
	print("%-10s %8d" % (item, item.get_cost()))