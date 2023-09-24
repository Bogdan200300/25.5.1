""" Modul 25 """

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_all_pets_has_diff_names(driver, my_pets):
   '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''

   # Устанавливаем явное ожидание
   element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

   # Сохраняем в переменную pet_data элементы с данными о моих питомцах
   pet_data = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу, остальное меняем
   # на пустую строку и разделяем по пробелу. Выбираем имена и добавляем их в
   # список pets_name.
   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      pets_name.append(split_data_pet[0])

   # Перебираем имена и если имя повторяется, то прибавляем к счетчику counter единицу.
   # Проверяем, если counter == 0, то повторяющихся имен нет.
   counter = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         counter += 1

   print(f'\nСовпадающих имен: {counter}')
   print(f'Все имена питомцев: {pets_name}')

   # Проверяем, есть ли повторяющиеся имена питомцев
   assert counter == 0


