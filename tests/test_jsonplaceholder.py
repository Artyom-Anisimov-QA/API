import pytest
import requests



#1. Тест на сравнение эквивалентности keys в json ответе

origin_response = {
   'id': 1,
   'title': '...',
   'body': '...',
   'userId': 1
   }

@pytest.mark.skip
@pytest.mark.smoke
@pytest.mark.regression
def test_api_compare_keys(api_jspl_url):
    response = requests.get(f'{api_jspl_url}/1')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    response1 = response.json()
    origin_response_list = list(origin_response.keys())
    response1_list = list(response1.keys())
    assert origin_response_list != response1_list, f'Ключи в {origin_response} не эквивалентны ключам в {response1}'


#2. Тест на проверку ключей в json ответе
@pytest.mark.smoke
@pytest.mark.regression
def test_api_keys_in_response(api_jspl_url):
    response = requests.get(f'{api_jspl_url}/1')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'userId' in  response.json()
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'body' in response.json()

#3. Тест на проверку списка всех ресурсов
@pytest.mark.smoke
@pytest.mark.regression
def test_api_listing_all_resources(api_jspl_url):
    response = requests.get(f'{api_jspl_url}')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'

#4. Проверка нескольких постов(позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'url',
    ['https://jsonplaceholder.typicode.com/posts/5', 'https://jsonplaceholder.typicode.com/posts/15', 'https://jsonplaceholder.typicode.com/posts/50']
)
def test_api_posts_positive(url):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'userId' in response.json()
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'body' in response.json()


#5. Проверка граничных значений (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'post_number',
    [1, 2, 3, 98, 99, 100]
                         )
def test_api_posts_positive(post_number):
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_number}')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'userId' in response.json()
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'body' in response.json()

#6. Проверка граничных значений (негативный)
@pytest.mark.regression
@pytest.mark.parametrize(
    'post_number',
    [-1, 0, 101, 102,'&']
                         )
def test_api_posts_negative(post_number):
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_number}')
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json; charset=utf-8'


#7. Тест на создание ресурса (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
def test_api_creat_resourse_positive(api_jspl_url, api_jspl_body, api_jspl_headers):
    response = requests.post(api_jspl_url, json=api_jspl_body, headers=api_jspl_headers)
    assert response.status_code == 201
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'title' in response.json()
    assert 'body' in response.json()
    assert 'userId' in response.json()
    assert 'id' in response.json()


#8. Тест на создание ресурса (негативный)
header = {'Content-type': 'text/html', 'charset': 'UTF-8'}

@pytest.mark.regression
def test_api_creating_resourse_negative(api_jspl_url, api_jspl_body):
    response = requests.post(api_jspl_url, json=api_jspl_body, headers=header)
    assert response.status_code == 201
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'title' not in response.json()
    assert 'body' not in response.json()
    assert 'userId' not in response.json()
    assert 'id' in response.json()


#9. Тест на изменение ресурса (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
def test_api_update_resourse_positive(api_jspl_url, api_jspl_body, api_jspl_headers):
    response = requests.put(f'{api_jspl_url}/1', json=api_jspl_body, headers=api_jspl_headers)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'foo' in response.json()['title']
    assert 'bar' in response.json()['body']


#10. Тест на изменение ресурса (негативный)
@pytest.mark.regression
def test_api_update_resourse_negative(api_jspl_url, api_jspl_body, api_jspl_headers):
    response = requests.post(f'{api_jspl_url}/1', json=api_jspl_body, headers=api_jspl_headers)
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json; charset=utf-8'


#11. Тест на частичное изменение ресурса
b = {
    'title': 'foo',
  }
@pytest.mark.smoke
@pytest.mark.regression
def test_api_update_resourse_positive1(api_jspl_url, api_jspl_headers):
    response = requests.put(f'{api_jspl_url}/1', json=b, headers=api_jspl_headers)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert 'foo' in response.json()['title']


#12. Тест граничных значений на фильтрацию по userId
# и наличию в списке ключей 'userId' c одинаковым значением (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('userId', [1, 2, 9, 10])
def test_api_filtering_positive(api_jspl_url, userId):
    response = requests.get(api_jspl_url, params={'userId': userId})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    user_id= data[0]['userId']
    for key in data:
        assert key['userId'] == user_id


#13. Тест граничных значений на фильтрацию по userId (негативный)
@pytest.mark.regression
@pytest.mark.parametrize('userId', [-1, 0, 'a', 11])
def test_api_filtering_negative(api_jspl_url, userId):
    response = requests.get(api_jspl_url, params={'userId': userId})
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


#14. Тест граничных значений на фильтрацию comments по postId
# и наличию в списке ключей (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('postId', [1, 2, 9, 10])
def test_api_filtering_comment_positive(api_jspl_url, postId):
    response = requests.get(api_jspl_url + f'/{postId} /comments')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data = response.json()
    assert isinstance(data, list)
    for dict in data:
        assert 'email' in dict
        assert 'name' in dict
        assert 'body' in dict
        assert 'id' in dict


#15. Тест граничных значений на фильтрацию comments (негативный)
@pytest.mark.regression
@pytest.mark.parametrize('postId', [-1, 0, 'a', 11])
def test_api_filtering_comment_negative(api_jspl_url, postId):
    response = requests.get(api_jspl_url + f'/{postId} /comments')
    data = response.json()
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert isinstance(data, list)
    assert len(data) == 0


#16. Тест граничных значений на фильтрацию photos по 'albumId'
# и наличию в списке ключей (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'url',
     ['https://jsonplaceholder.typicode.com/albums/1/photos',
      'https://jsonplaceholder.typicode.com/albums/2/photos',
      'https://jsonplaceholder.typicode.com/albums/99/photos',
      'https://jsonplaceholder.typicode.com/albums/100/photos'
      ]
    )
def test_api_filtering_album_positive(url):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data = response.json()
    assert isinstance(data, list)
    for dict in data:
        assert 'albumId' in dict
        assert 'url' in dict
        assert 'thumbnailUrl' in dict
        assert 'title' in dict
        assert 'id' in dict



#17. Тест граничных значений на фильтрацию photos (негативный)
@pytest.mark.regression
@pytest.mark.parametrize(
    'url',
     [
      'https://jsonplaceholder.typicode.com/albums/-1/photos',
      'https://jsonplaceholder.typicode.com/albums/0/photos',
      'https://jsonplaceholder.typicode.com/albums/a/photos',
      'https://jsonplaceholder.typicode.com/albums/101/photos',
      'https://jsonplaceholder.typicode.com/albums/102/photos'
      ]
    )
def test_api_filtering_album_negative(url):
    response = requests.get(url)
    data = response.json()
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert isinstance(data, list)
    assert len(data) == 0


#18. Тест граничных значений на фильтрацию albums по 'userId'
# и наличию в списке ключей (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('postId', [1, 2, 99, 100])
def test_api_filtering_album_positive(api_jspl_url_users, postId):
    response = requests.get(api_jspl_url_users + f'{postId}/albums')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data = response.json()
    assert isinstance(data, list)
    for dict in data:
        assert 'userId' in dict
        assert 'title' in dict
        assert 'id' in dict




#19. Тест граничных значений на фильтрацию comments (негативный)
@pytest.mark.regression
@pytest.mark.parametrize('postId', [-1, 0, 'a', 101])
def test_api_filtering_album_negative(api_jspl_url_users, postId):
    response = requests.get(api_jspl_url_users + f'{postId}/albums')
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


#20. Тест граничных значений на фильтрацию todos по 'albumId'
# и наличию в списке ключей (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('postId', [1, 2, 99, 100])
def test_api_filtering_todos_positive(api_jspl_url_users, postId):
    response = requests.get(api_jspl_url_users + f'{postId}/todos')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data = response.json()
    assert isinstance(data, list)
    for dict in data:
        assert 'userId' in dict
        assert 'title' in dict
        assert 'id' in dict
        assert 'completed' in dict


#21. Тест граничных значений на фильтрацию comments (негативный)
@pytest.mark.regression
@pytest.mark.parametrize('postId', [-1, 0, 'a', 101])
def test_api_filtering_todos_negative(api_jspl_url_users, postId):
    response = requests.get(api_jspl_url_users + f'{postId}/todos')
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


#22. Тест граничных значений на фильтрацию posts по 'userId'
# и наличию в списке ключей (позитивный)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    'url',
     ['https://jsonplaceholder.typicode.com/users/1/posts',
      'https://jsonplaceholder.typicode.com/users/2/posts',
      'https://jsonplaceholder.typicode.com/users/99/posts',
      'https://jsonplaceholder.typicode.com/users/100/posts'
      ]
    )
def test_api_filtering_posts_positive(url):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data = response.json()
    assert isinstance(data, list)
    for dict in data:
        assert 'userId' in dict
        assert 'title' in dict
        assert 'id' in dict


#23. Тест граничных значений на фильтрацию posts (негативный)
@pytest.mark.regression
@pytest.mark.parametrize(
    'url',
     [
      'https://jsonplaceholder.typicode.com/users/-1/posts',
      'https://jsonplaceholder.typicode.com/users/0/posts',
      'https://jsonplaceholder.typicode.com/users/a/posts',
      'https://jsonplaceholder.typicode.com/users/101/posts',
      'https://jsonplaceholder.typicode.com/users/102/posts'
      ]
    )
def test_api_filtering_posts_negative(url):
    response = requests.get(url)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0




