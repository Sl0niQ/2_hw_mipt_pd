import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.hub import Hub, Item

class TestHub(unittest.TestCase):
    #1
    def test_hub_singleton(self):
        'Проверка того что hub - синглтон'
        self.assertTrue(Hub() is Hub())

    #2
    def test_len(self):
        'Проверка того что при добавлении предметов меняется значение len(item)'
        h = Hub()
        h.clear()
        for i in range(5):
            h.add_item(Item())               
        self.assertEqual(len(h), 5)

class TestItem(unittest.TestCase):
    #3
    def test_item_id(self):
        """
        Проверка что разные экземпляры Item имеют разные ID
        """
        item1 = Item("Item 1")
        item2 = Item("Item 2")
        item3 = Item("Item 3")

        
        # Проверяем что все ID разные
        self.assertNotEqual(item1.item_id, item2.item_id)
        self.assertNotEqual(item1.item_id, item3.item_id)
        self.assertNotEqual(item2.item_id, item3.item_id)
        
        # Дополнительная проверка что ID не None
        self.assertIsNotNone(item1.item_id)
        self.assertIsNotNone(item2.item_id)
        self.assertIsNotNone(item3.item_id)

    #4
    def test_len(self):
        'Проверка того что при добавлении тэгов меняется значение len(item)'
        item1 = Item("Item 1")
        l = len(item1)
        item1.add_tags('test')
         # Проверяем что длина изменилась
        self.assertNotEqual(l, len(item1))
    
    #5    
    def test_equal_tags(self):
        'Проверка того что если к предмету добавить два идентичных тега - их колчество будет один'
        item1 = Item("Item 1")
        item1.add_tags('test')
        l = len(item1)
        item1.add_tags('test')
         # Проверяем что длина не изменилась
        self.assertEqual(l, len(item1))

class TestHubGetItem(unittest.TestCase):
    #6
    def test_valid_index(self):
        'Проверка корректности выбора элемента'
        items = [Item(f"item_{i}") for i in range(5)]
        hub = Hub()
        hub.clear()
        for i in range(5):
            hub.add_item(items[i])            
            self.assertIs(hub.get_item(i), items[i])
    #7    
    def test_negative_index(self):
        'Попытка ввода отрицательного индекса'
        items = [Item(f"item_{i}") for i in range(5)]
        hub = Hub()
        for i in range(5):
            hub.add_item(items[i])
        self.assertIsNone(hub.get_item(-1))

class TestFindById(unittest.TestCase):
    #8
    def test_find_existing_item(self):
        'Проверка поиска по существующему id'
        Item.reset_counter()
        items = [Item(f"item8_{i}") for i in range(5)]
        hub = Hub()
        hub.clear()
        for item in items:
            hub.add_item(item)
        #print(hub)
        self.assertEqual(hub.find_by_id(1), (1, "item8_1"))
        self.assertEqual(hub.find_by_id(2), (2, "item8_2"))
    #9
    def test_non_existing_item(self):
        'Проверка поиска по несуществующему id'
        print("Test 9")
        Item.reset_counter()
        items = [Item(f"item_{i}") for i in range(5)]
        hub = Hub()
        for i in range(5):
            hub.add_item(items[i])
        self.assertEqual(hub.find_by_id(99), (-1, None))

class TestFindByTags(unittest.TestCase):
    #10
    def test_find_items_with_existing_tags(self):
        'Поиск объектов с набором тегов'
        print("Test 10")
        hub = Hub()
        hub.clear()
        items = [Item(f"item_{i}") for i in range(5)]
        tags = ['tag 1', 'tag 2']
        items[2].add_tags(tags)
        for item in items:
            hub.add_item(item)
        found_items = hub.find_by_tags(tags)
        self.assertEqual(found_items, [items[2]])

    #11
    def test_find_items_with_wrong_tags(self):
        'Поиск среди объектов, не имеющих указанных тегов'
        print("Test 11")
        hub = Hub()
        hub.clear()
        items = [Item(f"item_{i}") for i in range(5)]
        tags = ['tag 1', 'tag 2']
        #items[2].add_tags(tags)
        for item in items:
            hub.add_item(item)
        found_items = hub.find_by_tags(tags)
        self.assertEqual(found_items, [])

class TestSetGetCost(unittest.TestCase):
    #12
    def test_set_get_cost(self):
        'Проверка изменения и получения цены объекта'
        print("Test 12")
        item = Item('apple')
        cost = 100
        item.set_cost(cost)
        self.assertEqual(item.get_cost(), cost)

class TestCompareItems(unittest.TestCase):
    #13
    def test_compare_items(self):
        'Проверка сравнения объектов по стоимости'
        print("Test 13")
        item1 = Item('apple', cost = 100)
        item2 = Item('apple', cost = 1000)
        self.assertTrue(item1 < item2)

class TestCopyItem(unittest.TestCase):
    #14
    def test_copy_item(self):
        'Проверка создания копии объекта с другим id'
        print("Test 14")
        Item.reset_counter()
        item1 = Item('apple', description = 'fruit', tags = ['tag1'], cost = 101)
        item2 = item1.copy_item()
        self.assertTrue(item1.name == item2.name)
        self.assertTrue(item1.description == item2.description)
        self.assertTrue(item1.dispatch_time == item2.dispatch_time)
        self.assertTrue(item1.tags == item2.tags)
        self.assertTrue(item1.cost == item2.cost)
        self.assertTrue(item1.item_id != item2.item_id)

class TestRemoveItem(unittest.TestCase):
    #15
    def test_remove_item(self):
        'Проверка удаления объекта по id или объекту'
        print("Test 15")
        Item.reset_counter()
        hub = Hub()
        hub.clear()
        items = [Item(f"item_{i}") for i in range(5)]
        for item in items:
            hub.add_item(item)
        # items[1] = 1 item_1
        self.assertTrue((1, items[1].name) == hub.find_by_id(1))
        self.assertTrue((2, items[2].name) == hub.find_by_id(2))
        hub.rm_item(1)
        self.assertTrue((-1, None) == hub.find_by_id(1))
        hub.rm_item(items[2])
        self.assertTrue((-1, None) == hub.find_by_id(2))

class TestDropItem(unittest.TestCase):
    #16
    def test_drop_item(self):
        'Проверка удаления объекта по id или объекту'
        print("Test 16")
        Item.reset_counter()
        hub = Hub()
        hub.clear()
        items = [Item(f"item_{i}") for i in range(5)]
        for item in items:
            hub.add_item(item)
        self.assertTrue((0, items[0].name) == hub.find_by_id(0))
        self.assertTrue((4, items[4].name) == hub.find_by_id(4))
        self.assertTrue((-1, None) == hub.find_by_id(5))
        hub.drop_items([items[0], items[4]])
        self.assertTrue((-1, None) == hub.find_by_id(0))
        self.assertTrue((-1, None) == hub.find_by_id(4)) 

class TestSetGetDate(unittest.TestCase):
    #17
    def test_set_get_cost(self):
        'Проверка изменения и получения даты синглтона'
        print("Test 17")
        hub = Hub()
        hub.clear()
        new_date = '2021-01-01'
        hub.set_date(new_date)        
        self.assertEqual(hub.get_date(), new_date)

class TestFindByDate(unittest.TestCase):
    #18
    def test_find_by_date(self):
        'Поиск объектов Item по dispatch_date'
        print("Test 18")
        Item.reset_counter()
        hub = Hub()
        hub.clear()
        items = [Item(item_name = f"item_{i}", dispatch_time = f"201{i}-01-01") for i in range(5)]
        for item in items:
            hub.add_item(item)
        test_1_items = [items[i] for i in range(3)] # 2010-01-01 2011-01-01 2012-01-01
        test_2_items = [items[i] for i in range(1, 4)] # 2011-01-01 2012-01-01 2013-01-01

        self.assertTrue(hub.find_by_date('2012-01-01') == test_1_items)
        self.assertTrue(hub.find_by_date('2011-01-01', '2013-01-01') == test_2_items)

class TestFindMostValuable(unittest.TestCase):
    #19
    def test_find_most_valuable(self):
        'Вывод заданного количества самых дорогих товаров'
        print("Test 19")
        Item.reset_counter()
        hub = Hub()
        hub.clear()
        items = [Item(item_name = f"item_{i}", cost = 5 * i) for i in range(10)]
        for item in items:
            hub.add_item(item)
        test_3_items = items[-1:-4:-1]
        self.assertTrue(test_3_items == hub.find_most_valuable(3))
        self.assertTrue(items[::-1] == hub.find_most_valuable(10))

#Item(self.item_name, self.description, self.dispatch_time, self.tags, self.cost)
if __name__ == '__main__':
    unittest.main()