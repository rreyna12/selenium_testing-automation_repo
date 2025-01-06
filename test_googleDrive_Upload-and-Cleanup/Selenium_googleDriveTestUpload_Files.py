"""
SUMMARY: All functions related to manipulation of files for the Selenium WebDriver Google Drive file upload test.
    **Because some of these functions don't have Selenium output, and instead have an expected python output, unit
    tests have been written.

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 1/6/2025
    Version: 1.0.1

    Updates: Fixed typo in gdrive_click_button_plus_new(), had added new parameter 'driver' but had typo in calling it
"""

import glob
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import os
import pyautogui
import pyperclip
import sys
from Selenium_googleDriveTestUpload_GoogleDrive_webItems import gdrive_click_button_plus_new
from Selenium_googleDriveTestUpload_Folders import navigate_to_folder_by_calc_url
from Selenium_googleDriveTestUpload_Connection import get_credentials_googledrive
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time  # driver implicit waits don't always seem to work

logger = logging.getLogger('seleniumTest.files')  # file logger


def create_file_newbutton(filename: str, filepath_abs: str, fld_uploadto_id: str, driver: webdriver
                          , navigate_to_googledrive: bool = False):
    """
    !!---Makes the assumption that you are already logged into Google Drive---!!
    Create a new file in Google Drive using Selenium to automate user's navigation to the requested folder, and then
    clicking through '+ New' button options.

    :param filename: The name of the file to be uploaded, including file type (ex: "testFile-1.txt")
    :type filename: str
    :param filepath_abs: The absolute file path of the file to be uploaded (ex: "C:/Windows/testFile-1.txt")
    :type filepath_abs: str
    :param fld_uploadto_id: The Google ID of the folder where the file should be uploaded
    :type fld_uploadto_id: str
    :param driver: A Selenium webdriver used to automate web clicks
    :type driver: webdriver
    :param navigate_to_googledrive: Does the func need to navigate to google drive before starting the click process?
        If program is on a Google Drive page - no need to provide this, the function will begin the click process.
        If not, pass in True - the function will then navigate to google drive first and then begin the click process.
    :type navigate_to_googledrive: bool
    """

    # Check if front slashes (/) were provided, if so, convert to backslashes, or this won't work (on Windows)
    filepath_abs = replace_frontslash(string=filepath_abs)

    logger.info(f"Attempting to create new file '{filename}' in folder ID '{fld_uploadto_id}'")

    # Navigate to the new folder (in order to upload file, need to be in folder)
    navigate_to_folder_by_calc_url(fld_id=fld_uploadto_id, driver=driver)

    # Click on '+ New' button; already on Google Drive page so don't need to navigate
    gdrive_click_button_plus_new(driver=driver, navigate_to_googledrive=navigate_to_googledrive)

    # Select "File upload" (sub-menu element)
    logger.debug("Selecting 'File upload' from the '+ New' sub menu")
    try:
        act = ActionChains(driver)
        # identify sub-menu element
        menuitem_newfile = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='File upload Alt+C then U']")))
        # define the action (click) and perform
        act.click(menuitem_newfile).perform()
        logger.info("Successfully (navigated to and) clicked sub-menu option 'File upload'")
        time.sleep(3)  # give file selection sub-menu time to appear; otherwise won't work
    except Exception as e:
        logger.error("Could not click on sub-menu option 'File upload'")
        logger.error(e)

    # Copy and paste in the absolute file path
    """ 
    **This is a windows explorer box so unable to interact with Selenium, but the windows explorer text box already 
    has the cursor focus, so can work with that
    """
    logger.info(f"Copying to clipboard: {filepath_abs}")
    pyperclip.copy(filepath_abs)  # save abs file path to the native clipboard
    logger.debug(f"Pasting into 'Open File' sub-window value {filepath_abs}")
    pyautogui.hotkey('ctrl', 'v')  # click ctrl+v; pyperclip.paste() didn't work

    time.sleep(1)  # give it time to paste
    logger.debug("Pressing enter for file upload")
    pyautogui.press('enter')
    sleep_sec = 5
    logger.debug(f"Sleeping for {sleep_sec} second(s) to allow the file to upload")
    time.sleep(sleep_sec)  # give it time to upload the file


def delete_file_googledrive_by_id(file_id: str):
    """
    Using Google API, deletes a Google Drive file by the folder's ID

    :param file_id:  Google ID of the file to be deleted
    :type file_id: str
    :return: Success value - returns True if file successfully deleted, False if not
    :rtype: bool
    """

    logger.info(f"Deleting file ID '{file_id}'...")

    # Validate if the file exists
    logger.debug("First validating if the file exists")
    exists = validate_file_exists(file_id=file_id)

    service = build("drive", "v3", credentials=get_credentials_googledrive())

    if exists is True:  # folder exists, delete
        response = service.files().delete(fileId=file_id).execute()

        # Validate if folder was deleted; if successful, the 'response' body contains an empty instance
        if not response:
            logger.info(f"File ID '{file_id}' successfully deleted.")
            result = True
        else:
            logger.error(f"Failed to delete file ID '{file_id}'")
            result = False

    else:  # file does not exist
        logger.warning(f"Unable to find and delete file ID '{file_id}'")
        result = False

    return result


def find_testfiles(filetype: str = ""):
    """
    Searches in the local ./testFiles folder for the requested file type and returns a list of all files.
    If file type is not provided, it will return a list of all files.

    :param filetype: - what file type you would like returned (ex: .txt, .csv, etc). If nothing provided, all file
        types will be returned
    :type filetype: str
    :return: Dictionary of file names and their absolute file paths; key = file name and value = absolute file path
        ex: {{'TestFile-1.txt': 'C:/testFiles/TestFile-1.txt'}}
    :rtype: dict
    """

    logmsg = "Getting list of requested file(s)"
    if not filetype:
        logmsg += ", no file type requested, will return all available files"
    else:
        logmsg += f", file type '{filetype}' requested."

    logger.info(logmsg)

    # Get current directory, since we'll need the full file paths to upload
    fp_testFiles = replace_backslash(os.getcwd()) + "/testFiles"

    # Get list of files, ignoring any sub-folders: https://www.geeksforgeeks.org/python-list-files-in-a-directory/
    if filetype == "":
        fp_testFiles_globsearch = f"{fp_testFiles}/*"
    else:  # file type provided
        fp_testFiles_globsearch = f"{fp_testFiles}/*.{filetype}"

    dict_files = {}
    for item in glob.glob(fp_testFiles_globsearch):
        item = replace_backslash(item)

        if os.path.isfile(item):  # remove sub-folders
            # adding to dict as {file name: file path}
            dict_files[item[(item.rfind("/")+1):]] = item

    logger.debug(f"Files found: {dict_files}")

    return dict_files


def get_file_googledrive_id(filename: str):
    """
    Using Google API, gets a file's Google Drive ID. Also includes the createdTime and parents fields to help
    distinguish between results if there is more than one result.

    :return: A dictionary of all applicable ID's in the following format:
    {'id': 'IDvalue', 'createdTime': 'datetime', 'parents': 'parentID'}
        * If there are multiple results, will return all results, with the createdTime and parentID to help identify
        * If there are no results, will return None
    :rtype: dict
    """

    logger.info(f"Getting file ID (via Google API) for '{filename}'")

    try:
        service = build("drive", "v3", credentials=get_credentials_googledrive())
        page_token = None

        while True:
            # Call the Drive v3 API
            results = (
                service.files()
                .list(q=f"mimeType != 'application/vnd.google-apps.folder' and name = '{filename}'",
                      spaces="drive",
                      fields="nextPageToken, files(id, createdTime, parents)",
                      # + ID for parent in case multiple results
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


def replace_backslash(string: str):
    """Replaces any backslashes (\) with a front slash (/).  The calls made in find_testfile return
    a variety of both \ and \\ in the results. Because a backslash needs to be escaped and '\\' must be used,
    simplifying, by just changing everything to a single front slash.

    :param string: String to be manipulated
    :type string: str
    :return: Returns a string value where all backslashes (\) have been replaced by front slashes (/)
    :rtype: str
    """

    logger.debug("Replacing any backslashes (\) with a front slash (/)")

    if string.find("\\") != -1:
        string = string.replace("\\", "/")

    return string


def replace_frontslash(string: str):
    """Replaces any front slashes (/) with a backslash (\).  When using Windows Explorer to upload a file to google
    drive, it won't accept a file path with a front slash.

    :param string: String to be manipulated
    :type string: str
    :return: Returns a string value where all front slashes (/) have been replaced by backslashes (\)
    :rtype: str
    """

    logger.debug("Replacing any front slashes (/) with a backslash (\)")

    if string.find("/") != -1:
        string = string.replace("/", "\\")

    return string


def validate_file_exists(filename: str = "", file_id: str = "", fld_id: str = ""):
    """
    Validates that a file exists, by either file name or file ID, with (optionally) folder location, using Google's API
        *if user does not have access to the file, it will show as not existing.

    :param filename: Name of the file, as it was uploaded, to be validated (ex: "testFile-1.csv)
    :type filename: str
    :param file_id: Google ID of the file to be validated
    :type file_id: str
    :param fld_id: Google ID of the folder where the file should be located (optional)
    :type fld_id: str
    :return: If the file exists
    :rtype: bool
    """

    # Validate that at least one of the file identification parameters was provided
    if filename:
        validateby = filename
        msg = f"Attempting to validate (via Google API) existence of file BY NAME '{filename}'"
    elif fld_id:
        validateby = file_id
        msg = f"Attempting to validate (via Google API) existence of file BY ID '{file_id}'"
    else:
        logger.error("ERROR: validate_file_exists requires either a name or ID, neither were provided")
        sys.exit()

    # Determine query
    query = ("mimeType != 'application/vnd.google-apps.folder' "  # .file too specific (ex: text/plain)
             "and trashed=false")

    if validateby == filename:
        query += f" and name = '{filename}'"
    elif validateby == file_id:
        query += f" and id = '{file_id}'"

    if fld_id == "":  # folder ID not provided
        msg += " ONLY; folder ID not provided."
        logger.info(msg)
    else:
        msg += f" in folder ID '{fld_id}'."
        logger.info(msg)
        query += f" and parents = '{fld_id}'"

    # Validate
    try:
        service = build("drive", "v3", credentials=get_credentials_googledrive())
        page_token = None

        while True:
            # Call the Drive v3 API
            results = (
                service.files()
                .list(q=query,
                      spaces="drive",
                      fields="nextPageToken, files(id, name, parents)",
                      pageToken=page_token)
                .execute()
            )

            items = results.get("files", [])

            # return results to user and log
            msg = f"File '{validateby}'"
            if fld_id != "":
                msg += f" in folder '{fld_id}'"

            if items:  # file found
                msg += " validated."
                logger.info(msg)

                return True
            else:
                msg += " could not be validated."
                logger.info(msg)

                return False
            if page_token is None:
                break
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
