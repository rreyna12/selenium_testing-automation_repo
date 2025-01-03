"""
SUMMARY: All functions related to interacting with any and all Google Drive web objects (ex: '+ New' button on
    left-side bar).

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 9/9/2024
    Version: 1.0.0
"""
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

logger = logging.getLogger('seleniumTest.googleDriveObjects')  # google drive objects logger


def gdrive_click_button_plus_new(driver: webdriver, navigate_to_googledrive: bool = False):
    """
    Clicks on the '+ New' button in the consistent left-hand sidebar of Google Drive.
    !!---Makes the assumption that you are already logged into google drive---!!

    REQUIRES that the user already be on a google drive page - so if navigate_to_googledrive is provided as True,
    then it will assume that it needs to navigate to the Google Drive "My Drive" page as a default; otherwise
    navigate_to_googledrive = False means that the script is already on a google drive page and this can be skipped.

    :param driver: Selenium webdriver used to automate web clicks
    :driver type: webdriver
    :param navigate_to_googledrive: Does the func need to navigate to google drive before starting the click process?
        If program is on a google drive page - no need to provide this, the function will begin the click process.
        If not, pass in True - the function will then navigate to google drive first and then begin the click process.
    :type navigate_to_googledrive: bool
    """
    logger.info("Clicking on Google Drive's '+ New' button in left-hand sidebar.")

    if navigate_to_googledrive is True:  # then need to navigate to a google drive page
        # Navigate to Google Drive 'My Drive' page
        logger.debug("Navigating to the 'My Drive' page")
        driver.get("https://drive.google.com/drive/my-drive")
        driver.implicitly_wait(5)

    # Click on "+ New" button
    logger.debug("Clicking on the '+ New' button")
    try:
        button_plusnew = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "button[guidedhelpid='new_menu_button']")))
        button_plusnew.click()
        # button_plusnew.click()  # when started testing, bug that required two clicks, seems to be fixed
        logger.info("Clicked on '+ New' button.")
    except Exception as e:
        logger.error("Could not click on '+ New' button.")
        logger.error(e)

    driver.implicitly_wait(1)
