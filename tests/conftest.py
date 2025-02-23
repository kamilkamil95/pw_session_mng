import requests
import pytest
from playwright.sync_api import sync_playwright


def get_auth_token():
    url = "http://127.0.0.1:5000/api/login"
    headers = {'Content-Type': 'application/json'}
    data = {
        'email': 'admin@admin.com',
        'password': 'admin'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        raise Exception("Failed to log in.")


@pytest.fixture(scope="function")
def page_logged():
    token = get_auth_token()
    if not token:
        raise Exception("No token received from API.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.add_cookies([{
            'name':'token',
            'value':token,
            'domain':'127.0.0.1',
            'path':'/',
            'httpOnly':False,
            'secure':False,
            'expires': -1
        }])
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page_not_logged():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()
