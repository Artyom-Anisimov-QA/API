import pytest
import requests

#1. Search for a brewery by ID
# https://api.openbrewerydb.org/v1/breweries/5128df48-79fc-4f0f-8b52-d06be54d0cec}
@pytest.mark.smoke
@pytest.mark.regression
def test_api_opdb_single_brewery(api_openbrewerydb):
    response = requests.get(api_openbrewerydb + '/5128df48-79fc-4f0f-8b52-d06be54d0cec')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    data  = response.json()
    assert data.get('id') == '5128df48-79fc-4f0f-8b52-d06be54d0cec'
    assert data.get('name') == '(405) Brewing Co'
    assert data.get('brewery_type') == 'micro'
    assert data.get('address_1') == '1716 Topeka St'
    assert data.get('address_2') is None
    assert data.get('address_3') is None
    assert data.get('city') == 'Norman'
    assert data.get('state_province') == 'Oklahoma'
    assert data.get('postal_code') == '73069-8224'
    assert data.get('country') == 'United States'
    assert data.get('longitude') == '-97.46818222'
    assert data.get('latitude') == '35.25738891'
    assert data.get('phone') == '4058160490'
    assert data.get('website_url') == 'http://www.405brewing.com'
    assert data.get('state') == 'Oklahoma'
    assert data.get('street') == '1716 Topeka St'


#2. Search for a brewery by ID (negative)
# https://api.openbrewerydb.org/v1/breweries/5128df48-79fc-4f0f-8b52-d06be54d0cec}
@pytest.mark.regression
def test_api_opdb_single_brewery(api_openbrewerydb):
    response = requests.get(api_openbrewerydb + '/5128df48-79fc-4f0f-8b52-d06be54d0cecc')
    assert response.status_code == 404
    assert response.json().get('message') == "Couldn't find Brewery"


#3. list of breweries by numbers (positive)
# https://api.openbrewerydb.org/v1/breweries?per_page={numbers}
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('input_number, output_number',
                         [({'per_page': 1}, 1),
                          ({'per_page': 2}, 2),
                          ({'per_page': 199}, 199),
                          ({'per_page': 200}, 200)]
                         )
def test_api_opdb_list_brewery_positive(input_number, output_number,api_openbrewerydb):
    response = requests.get(api_openbrewerydb, params=input_number)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert len(response.json()) == output_number


#4. list of breweries by numbers (negative)
# https://api.openbrewerydb.org/v1/breweries?per_page={numbers}
@pytest.mark.skip
@pytest.mark.regression
@pytest.mark.parametrize('per_page', [{'per_page': -1}, {'per_page': '&'}, {'per_page': 'a'}])
def test_api_opdb_list_brewery_negative(per_page, api_openbrewerydb):
    response = requests.get(api_openbrewerydb, params=per_page)
    assert response.status_code == 404


#5. list of breweries by numbers
# https://api.openbrewerydb.org/v1/breweries?per_page={numbers}

@pytest.mark.regression
@pytest.mark.smoke
def test_api_opdb_list_brewery_is_empty(api_openbrewerydb):
    response = requests.get(api_openbrewerydb, params={'per_page': 0})
    assert response.status_code == 200
    assert response.json() == []


#6. list of breweries by numbers (positive)
# https://api.openbrewerydb.org/v1/breweries?per_page={numbers}
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize('input_name, output_name',[
            ('10 Torr Distilling and Brewing', '10 Torr Distilling and Brewing'),
            ('(512) Brewing Co', '(512) Brewing Co'),
            ('1912 Brewing', '1912 Brewing')
            ]
            )
def test_api_opdb_list_brewery_positive(api_openbrewerydb, input_name, output_name):
    response = requests.get(api_openbrewerydb, params={'by_name': input_name})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json; charset=utf-8'
    assert response.json()[0]['name'] == output_name





