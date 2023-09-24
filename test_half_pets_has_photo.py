""" Modul 25 """

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_half_pets_has_photo(driver, my_pets):
    '''Поверяем что на странице со списком моих питомцев хотя бы у половины питомцев есть фото'''

    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')))

    # Получение списка всех обьектов питомцев
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

    # Проверка, что список своих питомцев не пуст
    assert len(all_my_pets) > 0

    # Сохраняем в переменную statistic элементы статистики
    statistic = driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Сохраняем в переменную images элементы с атрибутом img
    images = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # Получаем количество питомцев из данных статистики
    num_stat = statistic[0].text.split('\n')
    num_stat = num_stat[1].split(' ')
    num_stat = int(num_stat[1])

    # Находим половину от количества питомцев
    half = num_stat // 2

    # Находим количество питомцев с фотографией
    number_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_photos += 1

    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_photos >= half
    print(f'\nОбщее количество фото моих питомцев: {number_photos}')
    print(f'Половина карточек от числа моих питомцев: {half}')