"""
SUMMARY: All functions related to manipulation of folders for the Selenium WebDriver Google Drive file upload test.

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 8/27/2024
    Version: 1.0.0
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
from selenium import webdriver
from Selenium_googleDriveTestUpload_Connection import get_credentials_googledrive
from Selenium_googleDriveTestUpload_GoogleDrive_webItems import gdrive_click_button_plus_new
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time  # driver implicit waits don't always seem to work
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger('seleniumTest.folder')  # folder logger


def create_folder_newbutton(fldname: str, driver: webdriver, navigate_to_googledrive: bool = False):
    """
    !!---Makes the assumption that you are already logged into Google Drive---!!
    Create a new folder in Google Drive using Selenium to automate user's clicking through '+ New' button options.

    :param fldname: Name that the folder will be created with
    :type fldname: str
    :param driver: A Selenium webdriver that will be used to automate web clicks
    :type driver: webdriver
    :param navigate_to_googledrive: Does the func need to navigate to google drive before starting the click process?
        If program is on a Google Drive page - no need to provide this, the function will begin the click process.
        If not, pass in True - the function will then navigate to google drive first and then begin the click process.
    :type navigate_to_googledrive: bool
    """

    logger.info(f"Attempting to create new folder '{fldname}'")

    # Click on '+ New' button; should already be on a Google Drive page so don't need to navigate to gdrive
    gdrive_click_button_plus_new(driver=driver, navigate_to_googledrive=navigate_to_googledrive)

    # Select "New Folder" (sub-menu element)
    logger.debug("Selecting 'New Folder' from the '+ New' sub menu")
    try:
        act = ActionChains(driver)
        # identify sub-menu element
        menuitem_newfld = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='New folder Alt+C then F']")))
        """
        # move to element and click
        act.move_to_element(menuitem_newfld).click().perform()  # might not need to move to, might be able to just click
        """
        # define the action (click) and perform
        act.click(menuitem_newfld).perform()
        logger.info("Successfully (navigated to and) clicked sub-menu option 'New folder'")
    except Exception as e:
        logger.error("Could not click on sub-menu option 'New Folder'")
        logger.error(e)

    # Paste in new folder name
    time.sleep(2)  # if paste in too quickly, the default text "Untitled folder" won't be highlighted and overwritten
    logger.debug(f"Pasting in the requested folder name, '{fldname}'")
    driver.find_element(By.XPATH, '//input[@value="Untitled folder"]').send_keys(fldname)
    driver.implicitly_wait(1)

    # Click on "create" button
    logger.debug("Clicking on the 'create' button")
    try:
        button_newfld_create = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//span[text()='Create']")))
        # define the action (click) and perform
        act.click(button_newfld_create).perform()
        time.sleep(2)  # give google time to create the folder; driver.implicitly_wait() didn't work here
        logger.info("Successfully clicked on 'Create' button.")
    except Exception as e:
        logger.error("Could not click on 'Create' button.")
        logger.error(e)


def delete_folder_googledrive_by_id(fld_id: str):
    """
    Using Google API, deletes a Google Drive folder by the folder's ID

    :param fld_id: Google ID of the folder to be deleted
    :type fld_id: str
    :return: Success value - returns True if folder successfully deleted, False if not
    :rtype: bool
    """

    logger.info(f"Deleting folder ID '{fld_id}'...")

    # Validate if the folder exists
    logger.debug("First validating if the folder exists")
    exists = validate_folder_exists(fld_id=fld_id)

    service = build("drive", "v3", credentials=get_credentials_googledrive())

    if exists is True:  # folder exists, delete
        response = service.files().delete(fileId=fld_id).execute()

        # Validate if folder was deleted; if successful, the 'response' body contains an empty instance
        if not response:
            logger.info(f"Folder ID '{fld_id}' successfully deleted.")
            result = True
        else:
            logger.error(f"Failed to delete folder ID '{fld_id}'")
            result = False

    else:  # folder does not exist
        logger.warning(f"Unable to find and delete folder ID '{fld_id}'")
        result = False

    return result


def get_folder_googledrive_id(fldname: str):
    """
    Using Google API, gets a folder's Google Drive ID (can be used to calculate the URL to navigate to the folder).
    Also includes the createdTime and parents fields to help distinguish between results if there is more than one
    result

    :return: A dictionary of all applicable ID's in the following format:
    {'id': 'IDvalue', 'createdTime': 'datetime', 'parents': 'parentID'}
        * If there are multiple results, will return all results, with the createdTime and parentID to help identify
        * If there are no results, will return None
    :rtype: dict
    """

    logger.info(f"Getting folder ID (via Google API) for '{fldname}'")

    try:
        service = build("drive", "v3", credentials=get_credentials_googledrive())
        page_token = None

        while True:
            # Call the Drive v3 API
            results = (
                service.files()
                .list(q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{fldname}'",
                      spaces="drive",
                      fields="nextPageToken, files(id, createdTime, parents)",  # + ID for parent in case multiple results
                      pageToken=page_token)
                .execute()
            )
            items = results.get("files", [])
            if items:
                return items
            else:
                return None

            if page_token is None:
                break
    except HttpError as error:
        logger.error(f"An error occurred: {error}")


def navigate_to_folder_by_calc_url(fld_id: str, driver: webdriver):
    """Navigates to the provided folder URL by ID, if it exists, in Google Drive by calculating URL via Google API*
    and Selenium.  Will throw error if folder doesn't exist.
    Forcing to use ID vs name as a parameter because Google Drive allows for multiple folders with the same name.  This
    eliminates the question of which folder to use if there are multiple, as the user has to make that decision before
    calling this function

    *Since the purpose of this overall test is to specifically create a new folder and upload a file, using Google API
    for the folder nav. Function named appropriately where we can create a navigate_to_folder_via_user_clicks later
    if we do want to test out the user clicks to get there"""

    logger.info(f"Beginning process to navigate to requested folder '{fld_id}'")

    # First, validate that the folder even exists
    logger.debug(f"Validating existence of folder before navigating '{fld_id}'")
    exists = validate_folder_exists(fld_id=fld_id)
    if exists is False:
        logger.error(f"ERROR: Requested folder '{fld_id}' does not exist, unable to navigate to it.")

    # navigate to the URL using drive and folder ID
    # (ex: https://drive.google.com/drive/folders/11vRRYUOe2ogahi8AivTAgz4Ck8PcHvpy)
    logger.info("Navigating to the requested URL, using folder's google drive ID")
    url = f"https://drive.google.com/drive/folders/{fld_id}"
    logger.info(f"URL: {url}")
    driver.get(url)
    driver.implicitly_wait(5)


def validate_folder_exists(fldname: str = "", fld_id: str = ""):
    """Validate that a folder exists, by either name or ID (at least one is required), using Google's API
    *if user does not have access to the folder, it will show as not existing.

    :return: If the folder exists
    :rtype: bool
    """

    if fldname:
        validateby = fldname
        logger.info(f"Attempting to validate (via Google API) existence of folder BY NAME '{fldname}'")
    elif fld_id:
        validateby = fld_id
        logger.info(f"Attempting to validate (via Google API) existence of folder BY ID '{fld_id}'")
    else:
        logger.error("ERROR: validate_folder_exists requires either a name or ID, neither were provided")
        sys.exit()

    try:
        service = build("drive", "v3", credentials=get_credentials_googledrive())
        page_token = None

        while True:
            # Call the Drive v3 API
            if fldname:
                results = (
                    service.files()
                    .list(q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{fldname}' and trashed=false",
                          spaces="drive",
                          fields="nextPageToken, files(id, name)",
                          pageToken=page_token)
                    .execute()
                )
            elif fld_id:
                result_step1_byid = (
                    service.files()
                    .get(fileId=fld_id).execute()
                )
                results = (
                    service.files()
                    .list(q=f"name='{result_step1_byid['name']}' and mimeType = 'application/vnd.google-apps.folder' "
                            f"and trashed=false",
                          spaces="drive",
                          fields="nextPageToken, files(id, name)",
                          pageToken=page_token)
                    .execute()
                )

            items = results.get("files", [])
            if items:
                logger.info(f"Folder '{validateby}' validated")
                return True
            else:
                logger.warning(f"Folder '{validateby}' could not be validated.")
                return False

            if page_token is None:
                break
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
