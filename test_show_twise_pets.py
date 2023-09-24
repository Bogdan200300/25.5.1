""" Modul 25 """

from selenium.webdriver.common.by import By
from settings import valid_email, valid_password


def test_show_all_pets(driver):  # driver получаем из fixture

    #  Устанавливаем неявное ожидание
    driver.implicitly_wait(10)

    # Поиск поля ввода электронной почты, ввод email.
    myDynamicElement = driver.find_element(By.ID, 'email').send_keys(valid_email)

    #  Устанавливаем неявное ожидание
    driver.implicitly_wait(10)

    # Ищем поле ввода пароля, вводим свой пароль
    myDynamicElement = driver.find_element(By.ID, "pass").send_keys(valid_password)

    #  Устанавливаем неявное ожидание
    driver.implicitly_wait(10)

    # Ищем кнопку "Войти" и нажимаем на нее
    myDynamicElement = driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # if driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
    #     # Если мы на странице отображения моих питомцев, то сделать скриншот
    #     driver.save_screenshot('screenshots/result_petfriends.png')
    # else:
    #     raise Exception("login error")

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # В числе всех питомцев, находим карточки двух, содержащих все элементы, записываем элементы в переменные
    images = driver.find_elements(By.XPATH, '//div[69]/div[1]/img[1] | //div[75]/div[1]/img[1]')
    names = driver.find_elements(By.XPATH, '//div[69]/div[2]/h5[1] | //div[75]/div[2]/h5[1]')
    descriptions = driver.find_elements(By.XPATH, '//div[69]/div[2]/p[1] | //div[75]/div[2]/p[1]')
    # Организуем цикл, перебирающий элементы карточек (имя питомца, возраст и вид). Используем
    # переменную i и длину любого из массива найденных элементов (взяли name, но можно взять любую
    # из объявленных выше переменных, так как количество карточек равно количеству имён, картинок и описаний
    for i in range(len(names)):
        # Потому что на сайте https://petfriends.skillfactory.ru/all_pets не все питомцы имеют полностью
        # заполненную информацию (имя, порода, возраст, изображение), проверки будут падать,
        # но можно вместо len(names) - то есть количества всех питомцев на странице,
        # вставить меньшее количество питомцев для проверки, к примеру 1 или 2 и прогнать тест.

        # Берём элемент с номером i (картинка для i-й карточки питомца). Каждая картинка имеет атрибут
        # src, если была загружена, и не имеет его, если отсутствует для данного питомца. Поэтому
        # для проверки существования фотографии в карточке мы просто проверяем, что путь, указанный
        # в атрибуте src, не пустой.
        assert images[i].get_attribute('src') != ''

        # Берём i-го питомца и смотрим, что элемент, который должен содержать его имя, имеет
        # не пустой текст и т.д.
        assert names[i].text != ''
        assert descriptions[i].text != ''

        # Чтобы убедиться, что в данном элементе выводится и возраст, и вид питомца, мы ищем
        # в тексте этого элемента запятую, так как считаем её разделителем между этими двумя
        # сущностями. Этого всё ещё недостаточно, так как по отдельности ни возраст, ни вид
        # питомца могут не отдаваться сервером (в этом случае строка будет содержать только
        # один символ ,).
        # Чтобы убедиться, что в строке есть и возраст питомца, и его вид, мы разделяем строку
        # по запятой и ждём, что каждая из частей разделённой строки будет длиной больше нуля.
        # То есть в каждой части разделённого текста присутствуют символы. Именно это и будет
        # означать, что наша страница в карточке содержит и вид, и возраст питомца.
        assert ',' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0