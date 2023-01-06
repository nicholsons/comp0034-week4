from selenium.webdriver.chrome.options import Options
from dash.testing.application_runners import import_app
import pytest


def pytest_setup_options():
    options = Options()
    # Uncomment the following if testing on GitHub actions, the browser needs to run in headless mode
    # options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    return options


@pytest.fixture(scope="function")
def run_recycle_app(dash_duo):
    app = import_app("apps.recycle_app.recycle_dash_app")
    yield dash_duo.start_server(app)
