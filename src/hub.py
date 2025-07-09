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

from datetime import datetime
import re

class Hub:
	_items: list['Item'] = []
	_date = None
	_hub = None	

	def __new__(cls) -> 'Hub':
		"""
		Создает объект класса Hub и возвращает его. Синглтон.
		"""
		if cls._hub is None:			
			cls._hub = super().__new__(cls)			
			cls._date = datetime.now().isoformat()			
		return cls._hub

	def add_item(self, new_item) -> bool:
		"""
		Добавляет элемент в Hub
		Принимает объект класса Item
		Возвращает 
			True объект добавлен
			False ошибка: тип объекта не Item
		"""
		if not isinstance(new_item, Item):
			return False					
		self._items.append(new_item)		
		#print(f"add_item: item {new_item} has been added successfully")
		return True

	def get_item(self, position) -> 'Item':
		"""
		Поиск объекта в Hub по индексу
		Принимает значение индекса
		Возвращает объект класса Item, соответствующий индексу
		"""
		if position < 0 or position >= len(self._items):
			print(f"get_item: position ({position}) - no such item in hub")
			return None		
		return self._items[position]

	def find_by_id(self, id) -> tuple:
		"""
		Поиск по id
		Принимает значение id
		возвращает кортеж из двух значений - индекса и названия объекта
		Если объекта с id не существует, (-1, None)
		"""
		for i in range(len(self)):
			if self._items[i].item_id == id:
				return (i, str(self._items[i]))		
		return (-1, None)

	def find_by_tags(self, tags) -> list:
		"""
		Поиск товара по тегам
		Принимает: список тегов
		Возвращает: список товаров, имеющих все теги из полученного списка
		"""
		selected_items = []
		for item in self._items:
			#print(f"item = {str(item)}, tag = {tags}, _items.tags = {item.tags}")
			if all(tag in item.tags for tag in tags):
				#print(f"{item} contains all tags")
				selected_items.append(item)
		return selected_items

	def __len__(self) -> int:
		return len(self._items)

	def __repr__(self) -> str:
		hub_str = [item.name for item in self._items[:3]]
		return ', '.join(hub_str)

	def __str__(self) -> str:
		"""
		возвращает строку, содержащую id и название объектов склада
		"""
		item_name = [(item.item_id, item.name) for item in self._items]
		return f"items: {item_name}"

	def rm_item(self, i) -> bool:
		"""
		Удаляет элемент из списка _items
		Принимает индекс или объект
		Возвращает
			True, если объект удален
			False, если удаление невозможно
		"""
		if isinstance(i, int):
			if -1 < i < len(self):
				del self._items[i]
				return True
			else:
				print(f"Index {i} out of range")
				return False
		if isinstance(i, Item):
			cnt = 0
			for item in self._items:
				if i == item:
					del self._items[cnt]
					return True
				cnt += 1
			print(f"{i}: no such item in list")
			return False
		print(f"{i}: wrong type")
		return False

	def drop_items(self, items_for_drop: list) -> int:
		"""
		Удаляет все элементы из списка _items, присутствующие в заданном списке
		Принимает список объектов
		Возвращает количество удаленных объектов
		"""
		origin_len = len(self._items)
		self._items = [item for item in self._items if item not in items_for_drop]
		return origin_len - len(self._items)

	def clear(self) -> int:
		"""
		Очищает объект hub
		Возвращает количество удаленных товаров (элементов списка _items)
		"""
		origin_len = len(self._items)
		self._items = []
		self._id_counter = 0
		return origin_len

	def set_date(self, new_date) -> bool:
		"""
		Устанавливает новую дату создания объекта
		Принимает дату в формате YYYY-MM-DD
		Возвращает True, если дата изменена, и False, если нет
		"""
		if isinstance(new_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', new_date):
			self._date = new_date
			return True
		return False

	def get_date(self) -> str:
		"""
		Возвращает дату объекта
		"""
		return self._date

	def find_by_date(self, *args) -> list['Item']:
		"""
		Принимает дату или две даты в формате YYYY-MM-DD
		Возвращает лист всех Item, подходящих по дате. 
			Одна: возвращаются все items с датой раньше или равной ей
			Две даты: все items с датой в этом промежутке 
		В случае если передали слишком много параметров - ошибка
		"""
		num_of_args = len(args)
		if 0 < num_of_args < 3:
			if num_of_args == 1:
				dated_items = [item for item in self._items if item.dispatch_time <= args[0]]
			else:
				if args[0] > args[1]:
					begin = args[1]
					end = args[0]
				else:
					begin = args[0]
					end = args[1]
				dated_items = [item for item in self._items if begin <= item.dispatch_time <= end]
			return dated_items
		raise ValueError("Метод принимает 1 или 2 даты")

	def find_most_valuable(self, amount=1) -> list['Item']:
		"""
		Принимает количество товаров amount, которые нужно вывести
		Возвращает первые amount самых дорогих предметов на складе. Если предметов на 
		складе меньше чем amount - верните их все
		"""
		if not self._items:
			return []
		most_expensive_items = sorted(self._items)
		return most_expensive_items[-1:-(amount+1):-1]

class Item:
	_id_counter: int = 0
	#old def __init__(self, item_name = '', description = '', dispatch_time = '', tags = [], cost = 0, item_id = 0) -> None:
	def __init__(self, item_name = '', description = '', dispatch_time = '', tags = None, cost = 0) -> None:
		self.item_id: int = Item._id_counter
		self.name: str = item_name
		self.description: str = description
		self.dispatch_time: str = dispatch_time
		self.tags: list = tags if tags is not None else []
		self.cost: int = cost
		Item._id_counter += 1		

	def add_tags(self, tags_for_add) -> bool:
		"""
		Добавление одного или нескольких уникальных тегов
		Принимает строку или список
		Возвращает количество добавленных тегов
		"""
		count = 0
		if not isinstance(tags_for_add, (list, tuple, set)):
			tags_for_add = [tags_for_add]		
		for tag in tags_for_add:
			if tag not in self.tags:
				self.tags.append(tag)
				count += 1		
		return count		

	def rm_tags(self, tags_for_remove) -> bool:
		"""
		Удаление одного или нескольких тегов
		Принимает строку или список
		Возвращает True
		"""
		if not isinstance(tags_for_remove, (list, tuple, set)):
			tags_for_remove = [tags_for_remove]
		self.tags = [tag for tag in self.tags if tag not in tags_for_remove]
		return True

	def __len__(self) -> int:
		"""
		Принимает объект Item
		Возвращает длину объекта - количество элементов в списке tags
		"""
		return len(self.tags)

	def __repr__(self) -> str:
		"""
		Принимает объект Item
		Возвращает первые три тега объекта в виде строки
		"""
		item_str = self.tags[:3]
		return ', '.join(item_str)

	def __str__(self) -> str:
		"""
		Принимает объект Item
		Возвращает имя объекта в виде строки
		"""
		return self.name

	def set_cost(self, cost) -> bool:
		"""
		Изменение стоимости товара на складе
		Принимает: стоимость
		Возвращает:
			True если стоимость изменена
			False если стоимость некорректная
		"""		
		if cost < 0:
			print(f"Wrong value {cost} for cost")
			return False
		self.cost = cost
		return True

	def get_cost(self):
		"""
		Возвращает стоимость товара
		"""
		return self.cost

	def copy_item(self) -> 'Item':
		"""
		Принимает объект Item 
		Возвращает копию объекта с новым id
		"""
		new_item = Item(self.name, self.description, self.dispatch_time, self.tags, self.cost)
		return new_item

	def __lt__(self, other) -> bool:
		"""
		Переопределение функции сравнения для объектов класса Item
		"""
		#print('--------------__lt__-----------------------')
		if not isinstance(other, Item):
			return False
		return (self.cost < other.cost)
		"""	
		if self.cost < other.cost:			
			return True
		return False
		"""

	def __eq__(self, other) -> bool:
		"""
		Переопределение равенства для объектов класса Item
		"""
		if not isinstance(other, Item):
			return False
		return (self.name == other.name and
				self.description == other.description and
				self.dispatch_time == other.dispatch_time and
				self.tags == other.tags and
				self.cost == other.cost)

	@classmethod
	def reset_counter(cls):
		'Сброс значения id'
		cls._id_counter = 0

##############################END###################################

