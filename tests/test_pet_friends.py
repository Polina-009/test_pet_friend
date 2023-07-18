from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
pf = PetFriends()
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список"""

    # Cначала получаем api ключ и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Далее используя этот ключ запрашиваем список всех питомцев и проверяем что список не пустой.
    # Доступное значение параметра filter - 'my_pets' либо ''
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) >0
def test_add_new_pet_with_valid_key(name='Pip', animal_type='mouse', age='1', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Суперкот', 'кот', '3', 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
def test_successful_update_info_about_pet(name='Doggie', animal_type='dog', age='3'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев непустой, то меняем параметры питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем, что статус ответа равен 200 и данные о питомце обновились
        assert status == 200
        assert result['name'] == name
    # В обратном случае возвращаем ошибку "Моих питомцев нет"
    else:
        raise Exception('There is no my pets')

'''Домашнее задание 24.7.2'''
def test_add_new_pet_without_photo(name='Goray', animal_type='dog', age='1'):
    """Проверяем возможность добавления нового питомца без фотографии"""

    # Получаем ключ auth_key и добавляем нового питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем, что статус ответа равен 200 и данные о питомце добавлены
    assert status == 200
    assert result['name'] == name
def test_add_new_photo_of_pet(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления новой фотографии для своего питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев непустой, то меняем фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert len(result['pet_photo']) != 0
    # В обратном случае возвращаем ошибку "Моих питомцев нет"
    else:
        raise Exception('There is no my pets')
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем, что запрос api ключа с неверным email не выполняется"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'key' in result
def test_get_api_key_for_invalid_password(email=invalid_email, password=invalid_password):
    """Проверяем, что запрос api ключа с неверным паролем не выполняется"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'key' in result
def test_unsuccessful_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что список питомцев с неверным api ключом не выполняется.
    Для этого в файле api в методе get_list_of_pets меняем 'key' на неверный api,
    который указан в начале файла, для дальнейшего тестирования меняем данные на старые"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) >0
def test_create_pet_simple_with_negative_age(name='gggg', animal_type='poil', age='-1'):
    """Проверяем возможность добавления питомца с отрицательным возрастом"""

    # Получаем ключ auth_key и создаем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    # (в действительности отрицательного возраста быть не может - это баг)
    assert status == 200
    assert result['name'] == name
def test_create_pet_simple_without_name(name='', animal_type='poil', age='1'):
    """Проверяем возможность добавления питомца без имени"""

    # Получаем ключ auth_key и создаем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    # (в действительности питомца без имени быть не должно - это баг)
    assert status == 200
    assert result['name'] == name
def test_create_pet_simple_with_the_numerical_animal_type(name='gg', animal_type='34', age='1'):
    """Проверяем возможность добавления питомца с типом животного, который принимает численное значение"""

    # Получаем ключ auth_key и создаем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    # (в действительности тип животного не может быть числом - это баг)
    assert status == 200
    assert result['name'] == name
def test_create_pet_simple_with_name_in_сyrillic(name='пп', animal_type='cat', age='1'):
    """Проверяем возможность добавления питомца с именем, которое написано на кириллице"""

    # Получаем ключ auth_key и создаем нового питомца без фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_add_new_photo_of_pet_raw(pet_photo='images/cat1.raw'):
    """Проверяем, что фото питомца в формате raw возможно добавить"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев непустой, то меняем фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Сверяем полученный ответ с ожидаемым результатом
        # (в действительности фото по документации не может быть формата raw - это баг)
        assert status == 200
        assert len(result['pet_photo']) != 0
def test_add_new_photo_of_pet_webp(pet_photo='images/cat_fly.webp'):
    """Проверяем, что фото питомца в формате webp добавить невозможно"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев непустой, то меняем фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert len(result['pet_photo']) != 0
def test_add_new_pet_with_age_in_сyrillic(name='Pip', animal_type='mouse', age='пп', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с возрастом, которой принимает буквенное значение"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и создаем нового питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    # (в действительности возраст не может принимать буквенное значение - это баг)
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_with_name_of_257char(name='ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhv',
                                          animal_type='mouse', age='3', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с именем, состоящим из 257 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и создаем нового питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

