""" Modul 25 """

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_all_pets_present(driver, my_pets):
   '''Проверяем что на странице со списком моих питомцев присутствуют все питомцы'''

   # Устанавливаем явное ожидание
   element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')))

   # Получение списка всех обьектов питомцев
   all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

   # Проверка, что список своих питомцев не пуст
   assert len(all_my_pets) > 0

   list_pets = []
   for i in range(len(all_my_pets)):
      # Получение информации о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # Очистка от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # Добавление в список list_pets информации рода: имя, тип, возраст, по каждому питомцу
      list_pets.append(pet_info)

   # Подсчет количества питомцев в карточках
   number_of_pets = sum(1 for i in all_my_pets)

   # Сохранение в переменную statistic элементов статистики
   statistic = driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

   # Получение количества питомцев из данных статистики
   num_stat = statistic[0].text.split('\n')
   num_stat = num_stat[1].split(' ')
   num_stat = int(num_stat[1])

   # Проверка равенства количества питомцев в карточках с количеством питомцев из данных статистики
   assert number_of_pets == num_stat
   print(f'\nКоличество питомцев в карточках: {number_of_pets} == Количество питомцев из статистики: {num_stat}')