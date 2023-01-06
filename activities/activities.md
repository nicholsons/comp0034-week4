# Testing Dash apps

Contents:

- [Activity introduction](#activity-introduction)
- [Setup](#setup)
- [Unit testing callbacks with dash.Testing](#unit-testing-callbacks-with-dashtesting)
- [End to end testing with Selenium](#end-to-end-testing-with-selenium)

## Activity introduction

This activity will introduce you to testing a Dash app using pytest and Selenium webdriver. You will test the Dash app in the `src/apps/recycle_app` directory.

The activity assumes you completed the setup instructions in README.md. If you have not, please do so before starting otherwise you are likely to experience issues with imports during testing.

The activity is based on the guidance on testing given in the [Dash documentation](https://dash.plotly.com/testing).

In COMP0035 you learned how to use pytest to create tests. This style of testing would be useful to test the functions in `recyclingchart.py` and `recyclingdata.py`. However, the structure
of Dash (or any web app) is such that it would be difficult to create unit tests in the same way.

A more useful approach for the Dash app would be to test components, or integration testing. That is, to run the Dash app and test that it can be used to complete the functions you defined in your user stories or use cases (in the COMP0035 coursework 2).

To do this you will use an additional library called Selenium. Selenium allows you to run tests automatically in the browser, that is you simulate the behaviour of a user carrying out specific actions in the browser and then use assertions to verify particular conditions or state.

Selenium can be used with a number of test libraries, we will use pytest since you used this in COMP0035, and it is recommended in the Dash documentation.

**NOTE: Writing tests for your Dash app for coursework 1 is only required for groups**

## Setup

### Install the testing packages

Enter `pip install pytest selenium pytest-cov dash[testing]` in a terminal/console within your venv.

## Download and install the correct version of Chromedriver for your computer

You will need to use the [Chrome browser for testing Dash](https://dash.plotly.com/testing), though Selenium supports a
number of browsers.

Check your version of Chrome in the Chrome settings/preferences 'About Chrome'.

Go to [Chrome driver downloads](https://sites.google.com/chromium.org/driver/downloads) and select the version for your
version Chrome.

In the next window you then need to download the correct driver for your operating system.

The [Selenium documentation](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) explains where to place it in Windows and how to add it to the path, and for macOS.

My experience on a MacBook was that I had to complete the following steps:

- Download the driver
- Try to open the driver from the download directory, this prompts you to change the security settings for the file (
  System Settings | Security & Privacy | General and then click on 'Open Anyway').
- Close the driver
- Move the driver from downloads to `usr/local/bin`  (I use this location as it is already in PATH)

## End to end testing with Selenium

### Test code structure

Boilerplate code for creating a test is given in the Dash documentation.

This was used when writing [test/test_recycle_app/test_recycle_app.py](/test/test_recycle_app/test_recycle_app.py)`. Open this file now before reading the rest of this document.

### Name the test

In the documentation the test function name follows this pattern: test_{tcid}_{test title}.

The test case ID (tcid) is an abbreviation pattern of mmffddd => module + file + three digits.

You do not have to follow this pattern if you are following a different naming convention for your tests. As you should
remember from COMP0035 it is a good idea to start with `test_` as many test runners will autodetect tests based on this
naming pattern. The name of the test should also indicate what the test does.

I have used a slightly different 'tcid' using an abbreviation for the app plus 3 digits.

You should see that the first test is named `def test_rec001_h1textequals(dash_duo):`

## Create the dash app

The boilerplate code suggests that you define and create the app in every test case. This would lead to a lot of
repetition and become difficult to maintain. Instead, create the app by using the `import_app` function which is in the
application_runners module, this only works if the file that runs the dash app is
called `app.py` ([see community post here](https://community.plotly.com/t/how-you-can-integration-test-your-app-by-dash-testing/25002)):

```python
from dash.testing.application_runners import import_app


def test_spa001_h1textequals(dash_duo):
    app = import_app("apps.recycle_app.recycle_app")
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

## Unit testing callbacks with dash.Testing

Code from the Dash testing tutorial has been recreated in [test/test_recycle_app/test_callbacks.py](/test/test_app/test_callbacks.py)

TODO: Write this section of the tutorial!
