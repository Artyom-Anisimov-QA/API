import pytest


#_____Fixtures for https://dog.ceo/dog-api/_______
@pytest.fixture
def api_dog_url():
    return 'https://dog.ceo/api/breeds'

#_____Fixtures for https://jsonplaceholder.typicode.com/_______
@pytest.fixture
def api_jspl_url():
    return 'https://jsonplaceholder.typicode.com/posts'

@pytest.fixture
def api_jspl_url_users():
    return 'https://jsonplaceholder.typicode.com/users/'

@pytest.fixture
def api_jspl_body():
    return {'title': 'foo', 'body': 'bar','userId': 1}

@pytest.fixture
def api_jspl_headers():
    return {'Content-type': 'application/json', 'charset': 'UTF-8'}

#_____Fixtures for https://www.openbrewerydb.org/_______
@pytest.fixture
def api_openbrewerydb():
    return 'https://api.openbrewerydb.org/v1/breweries'



#_________________.addoption______________________
def pytest_addoption(parser):
    parser.addoption(
        '--url',
        default = 'https://ya.ru',
        choices = ['https://ya.ru', 'https://ya.ru/sfhfh']
    )
    parser.addoption(
        '--status_code',
        default = '200',
        choices = ['200', '404']
    )

#_____Fixtures for .addoption/____________________
@pytest.fixture
def base_url(request):
    return request.config.getoption('--url')

@pytest.fixture
def status_code(request):
    return int(request.config.getoption('--status_code'))
