import pytest
import uuid
from selenium import webdriver  # подключение библиотеки selenium
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password
import time
import datetime

base_url = 'https://petfriends.skillfactory.ru/'

# Pre-request
# webdriver_auto_update - способ автоматической загрузки драйвера Chrome.
from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate

def driver_update():
    # Target directory to store chromedriver
    driver_directory = r"D:\Education\IT\Modul_24_selenium\chromedriver"
    # r либо \\ - это необработанная строка, против ошибки DeprecationWarning: invalid escape sequence

    # Create an instance of WebdriverAutoUpdate
    driver_manager = WebdriverAutoUpdate(driver_directory)

    # Call the main method to manage chromedriver
    driver_manager.main()

    return driver_update

@pytest.fixture()
def driver(request):
    driver = webdriver.Chrome()

    # Задаем нужный размер экрана
    driver.maximize_window()
    # driver.set_window_size(1800, 1200)  # для теста, когда все элементы сдвигаются

    # Переходим на страницу авторизации PetFriends
    driver.get(f'{base_url}/login')

    yield driver

    # Post-request
    # Этот код выполнится после отрабатывания теста:
    if request.node.rep_call.failed:
       # Сделать скриншот, если тест провалится:
       try:
           driver.execute_script("document.body.bgColor = 'green';")
           # Меняется цвет фона для контрастности при помощи команды javascript и делается скриншот.

           # Создаем папку screenshots и кладем туда скриншот с генерированным именем:
           driver.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

           # Для дебагинга, печатаем информацию в консоль
           print('URL: ', driver.current_url)
           print('Browser logs:')
           # browser.get_log выводит в системную консоль логи из консоли веб-браузера
           for log in driver.get_log('browser'):
               print(log)
       except:
           driver.quit()

@pytest.fixture()
def my_pets(driver):
    time.sleep(1)  # небольшая задержка

    # Ищем поле ввода электронной почты, очищаем его, а затем вводим свой email,
    login = driver.find_element(By.ID, "email")
    login.clear()
    login.send_keys(valid_email)

    # Ищем поле ввода пароля, очищаем его, а затем вводим свой пароль,
    password = driver.find_element(By.ID, "pass")
    password.clear()
    password.send_keys(valid_password)

    # Ищем кнопку "Войти" и нажимаем на нее
    butt_ent = driver.find_element(By.XPATH, "//button[@type='submit']")
    butt_ent.click()

    time.sleep(1)  # небольшая задержка

    # Ищем кнопку "Мои питомцы" и нажимаем на нее
    butt_my_pets = driver.find_element(By.LINK_TEXT, "Мои питомцы")
    butt_my_pets.click()

    time.sleep(1)  # небольшая задержка

    if driver.current_url == f'{base_url}my_pets':
        # Если мы на странице отображения моих питомцев, то сделать скриншот
        driver.save_screenshot('screenshots/result_petfriends.png')
    else:
        raise Exception("login error")

@pytest.fixture(autouse=True)  # не работает со scope='class'
def request_fixture(request):
    if 'Pet' in request.function.__name__:
        print(f'\nЗапущен тест {request.function.__name__} из сьюта Дом Питомца\n')
    if 'get' in request.function.__name__:
        print(f'\nЗапущен тест {request.function.__name__} c методом GET\n')

    print('Test name: ', request.function.__name__)
    # print(request.fixturename)   # название фикстуры
    print('Scope: ', request.scope)
    print('Class name: ', request.cls)
    print('Module name: ', request.module.__name__)
    print('File path: ', request.fspath)
    if request.cls:  # почему-то не работает
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"

@pytest.fixture(autouse=True)
def time_out():
    start_time = datetime.datetime.now()
    yield
    end_time = datetime.datetime.now()
    print(f"\nВремя, затраченное на тест: {end_time - start_time}")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep