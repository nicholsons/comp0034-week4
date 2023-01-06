# Integration testing for Dash apps

## Introduction

This activity will introduce you to testing your Dash app using pytest and Selenium webdriver. You will test the Dash
app in the `/apps/recycle_app` directory.

The activity is based on the guidance on testing given in the [Dash documentation](https://dash.plotly.com/testing).

In COMP0035 you learned how to use pytest to create unit tests.

Unit testing would be useful to test the functions in `recyclingchart.py` and `recyclingdata.py`, however the structure
of Dash is such that it would be difficult to create unit tests in the same way.

A more useful approach for the Dash app would be to test components, or integration testing. That is, to run the Dash
app and test that it can be used to complete the functions you defined in your user stories or use cases (in the
COMP0035 coursework 2).

To do this you will use an additional library called Selenium. Selenium allows you to run tests automatically in the
browser, that is you simulate the behaviour of a user carrying out specific actions in the browser and then use
assertions to verify particular conditions or state.

Selenium can be used with a number of test libraries, we will use pytest since you used this in COMP0035, and it is
recommended in the Dash documentation.

**NOTE: Writing tests for your Dash app for coursework 1 is only required for groups of 3-4.**

## Install pytest and selenium, and configure your IDE to run pytest for the project

Pytest was included in the requirements.txt for the repository. If you did not install when you created the project then you will need to do so now e.g. `pip install pytest pytest-cov selenium`.

You may also need to configure your IDE to use pytest to run the tests. This was covered in COMP0035; or refer to the documentation for your IDE.

## Install dash testing

Enter `pip install dash[testing]` in a terminal/console within your venv. In PyCharm you can open the Terminal by going
to View - Tool Windows - Terminal and then enter `pip install dash[testing]`

## Download and install the correct version of Chrome driver for your computer

You will need to use the [Chrome browser for testing Dash](https://dash.plotly.com/testing), though Selenium supports a
number of browsers.

Check your version of Chrome in the Chrome settings/preferences 'About Chrome'.

For example, mine is currently: Version 97.0.4692.71

Go to [Chrome driver downloads](https://sites.google.com/chromium.org/driver/downloads) and select the version for your
version Chrome.

In the next window you then need to download the correct driver for your operating system.

The [Selenium documentation](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) explains where to
place it in Windows and how to add it to the path, and for macOS.

My experience on a MacBook was that I had to complete the following steps:

- Download the driver
- Try to open the driver from the download directory, this prompts you to change the security settings for the file (
  System Settings | Security & Privacy | General and then click on 'Open Anyway').
- Close the driver
- Move the driver from downloads to `usr/local/bin`  (I use this location as it is already in PATH)

# Create the first test

Boilerplate code for creating a test is given in the Dash documentation.

This was used when writing [tests/test_recycle_app.py](../tests/test_recycle_app.py)`. Open this file now before reading the rest of this document.

## Name the test

In the documentation the test function name follows this pattern: test_{tcid}_{test title}.

The test case ID (tcid) is an abbreviation pattern of mmffddd => module + file + three digits.

You do not have to follow this pattern if you are following a different naming convention for your tests. As you should
remember from COMP0035 it is a good idea to start with `test_` as many test runners will autodetect tests based on this
naming pattern. The name of the test should also indicate what the test does.

I have used a slightly different 'tcid' using an abbreviation for the app plus 3 digits.

You should see that the first test is named `def test_spa001_h1textequals(dash_duo):`

### Create the dash app for the test

The boilerplate code suggests that you define and create the app in every test case. This would lead to a lot of
repetition and become difficult to maintain. Instead, create the app by using the `import_app` function which is in the
application_runners module, this only works if the file that runs the dash app is
called `app.py` ([see community post here](https://community.plotly.com/t/how-you-can-integration-test-your-app-by-dash-testing/25002)):

```python
from dash.testing.application_runners import import_app


def test_rec001_h1textequals(dash_duo):
    app = import_app("recycle_app.recycle_app")
```

The docstring for the `import_app` function explains how to reference your dash app:

```python
"""Import a dash application from a module. The import path is in dot
    notation to the module. The variable named app will be returned.

    :Example:

        >>> app = import_app("my_app.app")

    Will import the application in module `app` of the package `my_app`.

    :param app_file: Path to the app (dot-separated).
    :type app_file: str
    :param application_name: The name of the dash application instance.
    :raise: dash_tests.errors.NoAppFoundError
    :return: App from module.
    :rtype: dash.Dash
    """
```

Further, you could create a fixture in `conftest.py` to create the app and then use in your test functions if you prefer:

```python
from dash.testing.application_runners import import_app


@pytest.fixture(scope="function")
def run_recycle_app(dash_duo):
    app = import_app("apps.recycle_app.recycle_dash_app")
    yield dash_duo.start_server(app)
```

### Create and configure the webdriver

You do not need to explicitly create and declare the Selenium webdriver. This is created for you using the Chrome driver as default. If you want to use a different driver e.g. Firefox, you will need to read
the [Plotly Dash documentation](https://dash.plotly.com/testing) for how to do this.

If you need to configure the Chrome driver (and you will need to do this if you want to run the tests in GitHub) then you can modify the Chrome Options by adding a function (not a fixture) in `conftest.py`, for example the following would run the driver in headless mode which you need for remote execution on GitHub.

Comment out (i.e. add a `#` before) the headless option now so that you can see the tests running in a browser on your computer.

```python
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    options = Options()
    # Uncomment the following if testing on GitHub actions, the browser needs to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return options
```

## Waits

If you recall, Selenium webdriver loads the web app, however the tests could run before the page has finished rendering
and a test may fail as a given element was not yet available. To avoid this you can
use [waits](https://www.selenium.dev/documentation/webdriver/waits/), either to wait for a set period of time or to wait
for a particular event on the page.

In the first test we wait for the first `<h1>` element to be available:

```python
dash_duo.wait_for_element("h1", timeout=4)
```

You can also access the [implicit waits](https://www.selenium.dev/documentation/webdriver/waits/#implicit-wait) by
using `dash_duo.driver` which exposes the methods from the selenium API. For
example: `dash_duo.driver.implicitly_wait(5)`

## Find an element and property to check

In the first test, the nest step is to find the text value of the h1 heading like this:
`h1_text = dash_duo.find_element("h1").text`.

Finding an element, or all elements, can be done using tags, ids, classes.
The [location strategies are explained in the documentation](https://www.selenium.dev/documentation/webdriver/elements/)
along with examples of Python code.

As well as finding an element, you can also interact with an element, for example fill in details of a form, click on a
link or a button. Some of these are shown in the example tests in `test_recycle_app.py` and there are further examples
in the [selenium documentation](https://www.selenium.dev/documentation/webdriver/elements/).

## Write the assertion(s)

We covered writing assertions in COMP0035. If you recall, pytest uses `assert` for most assertions (rather than different
assertion types such as assert_equal, assert_contains etc.).

For the first test we 'assert' that the text in the `<h1>` element includes the text 'Waste and recycling'. However, the
bootstrap style that is applied to this element converts the text to uppercase, so the test would fail.

Instead, a step has been added to compare the strings ignoring the case using the python function `.casefold()`. There
are other techniques you could use such as `.upper()`, `.lower()`, or REGEX pattern matching.

```python
h1_text = dash_duo.find_element("h1").text
assert h1_text.casefold() == 'Waste and recycling'.casefold()
```

## Run the tests

Run the tests using the appropriate pytest run method for your IDE (covered in COMP0035) or from the terminal e.g.:

```python -m pytest -v```

# Add a test

Try and add at least one more test to `test_recycle_app.py`.

# Notes for coursework 1

In addition to the above you may also want to include:

- unit tests for any 'helper' functions that are not part of the Dash app itself
- running the tests from GitHub Actions

## Consider writing unit tests for 'helper' functions

If you have written helper or utility functions for creating charts, preparing data etc. then you could also test these using the
unit testing techniques covered in coursework 1.

## Consider running the tests using GitHub Actions

Using GitHub Actions was covered in COMP0035, however there are a couple of changes you will need to made in order to
run the Dash tests that use selenium.

### Step 1: Create a fixture to run the tests in headless mode

When running the tests on a remote server the browser can't be displayed on a screen, so it needs to be configured to be
used in `headless` mode which requires two settings. The Dash testing documentation suggests headless mode is set by
default, so you only need to disable the gpu, however explicitly setting headless as well isn't an issue so the code
below should work. To do this you will need to create a pytest fixture in `conftest.py` to set the ChromeDriver options.

Add the following to a file named `conftest.py` in your test directory:

```python
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return options
```

I also tried to extract the server creation to a fixture which seems to work. The full `conftest.py` as used in
the [completed example repository](https://github.com/nicholsons/comp0034_week5_complete/blob/master/tests/conftest.py)
is:

```python
import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    options = Options()
    # Uncomment the following if testing on GitHub actions, the browser needs to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return options


@pytest.fixture(autouse=True)
def run_recycle_app(dash_duo):
    # The import_app function will only work if the dash app code is in a file named app.py
    app = import_app("apps.recycle_app.app")
    yield dash_duo.start_server(app)
```

### Step 2: Create a GitHub Actions workflow that runs the selenium browser tests

The use of GitHub Actions for automatically running tests was covered in COMP0035. You could also apply this to run the
Dash tests automatically.

The GitHub Actions steps are not repeated in full here (see COMP0035 or use GitHub documentation). However, you need to
install `dash[testing]` explicitly so this is explained below.

- Go to your GitHub repository and find the Actions tab
- The Getting Started... screen provides an option to search, search and find 'python application' then select Configure
  on that option in the search results
- A workflow definition in YAML is created. You will need to make a few changes:
  - You may wish to change the workflow name
  - Change the version of Python that is used to match the version you are using to develop (the default is currently
      3.10)
  - Add in a line of code after the installation of the libraries in requirements.txt to
      install `pip install dash[testing]`
  - You don't need to install ChromeDriver as the default environment in GitHub already installs this for you.
  - Change the line of code that runs the pytest to `python -m pytest` and not simply `pytest`. This
      is [explained here](https://docs.pytest.org/en/6.2.x/goodpractices.html#tests-outside-application-code).
- Select 'Start commit' once you finish editing the workflow.
- Go back to the Actions tab. The workflow is likely to be still running, once it finished click on it and expand the
  build steps to check there are no errors.

You can check the workflow in the completed example
repository [here](https://github.com/nicholsons/comp0034_week5_complete/blob/master/.github/workflows/python-app.yml).
