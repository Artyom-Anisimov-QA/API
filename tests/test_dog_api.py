import requests
import pytest


#1. Проверка ключей в json() ответе
@pytest.mark.smoke
@pytest.mark.regression
def test_api_get_key(api_dog_url):
    response = requests.get(f'{api_dog_url}/image/random')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    assert 'message' in response.json(), f'Ответ должен содержать ключ message'
    assert 'status' in response.json(), f'Ответ должен содержать ключ message'



#2. Проверка количества ключей объекта ['message']
@pytest.mark.smoke
@pytest.mark.regression
def test_api_get_list_all_breeds(api_dog_url):
    response = requests.get(f'{api_dog_url}/list/all')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    json_data = response.json()['message']
    count_object = len(json_data)
    assert count_object == 107, f'Количество ключей в [message] должно быть 107'



#3. Проверка заданного количества ключей объекта  ['message'] в эндпоинте
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'api_dog_url, input_object, expected_object',
    [
        ('https://dog.ceo/api/breeds', 50, 50)
    ],
)
def test_api_get_numbers(api_dog_url, input_object, expected_object):
    response = requests.get(f'https://dog.ceo/api/breeds/image/random/{input_object}')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    input_object = len(list(response.json()['message']))
    assert input_object == expected_object, f'В ответе пришло {input_object} значений объекта [message], хотя ожидается {expected_object}'


#4. Проверка ввода не корректого url
@pytest.mark.regression
def test_api_url_negative(api_dog_url):
    response = requests.get(f'{api_dog_url}/image/randsukn')
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    assert response.json()['status'] == 'error'
    assert 'No route found for' in response.json()['message']


#5. Тест получения случайного изображения породы собак (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'breed',
    ['dalmatian', 'retriever']
)
def test_random_image_positive(breed):
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    assert response.json()['status'] == 'success'

#6. Тест получения случайного изображения породы собак (негативный)
@pytest.mark.regression
@pytest.mark.parametrize(
    'breed',
    ['dalmatiaaeuiv']
)
def test_random_image_negative(breed):
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'
    assert response.encoding == 'utf-8'
    assert response.json()['status'] == 'error'
    assert response.json()['message'] == 'Breed not found (master breed does not exist)'









