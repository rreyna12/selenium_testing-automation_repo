"""
Summary: Simple first Selenium project per walk through steps on
Selenium's site: https://www.selenium.dev/documentation/webdriver/getting_started/first_script/

    TEST: Look for board game "Betrayal at House on the Hill" on Amazon and
        validate results.

        Steps:
            - Open Amazon
            - Search for "Betrayal at House on the Hill"
            - Validate page title
            - Close test

NOTES:
    - make sure that you:
        - install Selenium (pip install Selenium)
        - if using PyCharm, install Selenium package by clicking on Python version in bottom right corner and
            selecting Interpreter Setting > Python Interpretor
    - used Chrome's Inspect and CSS Selector to determine object names
    - this test will fail if run too frequently, as Amazon's "validate you're not a robot" page will come up

VERSION INFO:
    Created by R. Reyna
    Date: 8/20/2024
    Version: 1.0.0
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

searchPhrase = "Betrayal at House on the Hill"

# Start Chrome session
driver = webdriver.Chrome()

# Open Amazon's webpage
driver.get("https://www.amazon.com/")

driver.implicitly_wait(0.5)  # adding so can view test happening in real time

# Search Amazon for search term
text_search_box = driver.find_element(by=By.NAME, value="field-keywords")
submit_search_button = driver.find_element(by=By.CSS_SELECTOR, value="#nav-search-submit-button.nav-input.nav-progressive-attribute")

text_search_box.send_keys(searchPhrase)
submit_search_button.click()

driver.implicitly_wait(0.5)  # adding so can view test happening in real time

# Validate title page
title = driver.title
try:
    assert searchPhrase in title
    print('Title Assertion test pass')
except Exception as e:
    print('Title Assertion test failed', format(e))

# Close test
driver.quit()
