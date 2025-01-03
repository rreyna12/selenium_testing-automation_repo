"""
SUMMARY: Executes the modules to test Google Drive's Create folder and Upload file features using Selenium.

    TEST STEPS*:
        - Open/log into Google Account
        - Open up Google Drive
        - Get test text file from the local ./testFiles folder
        - Create Google Drive folder "Testing Folder (Selenium)"
        - Validate the folder was created successfully (via Google API)
        - Upload file to Google Drive folder "Testing Folder (Selenium)"
        - Validate the file was uploaded successfully and return results to user
        - Close test
    *Clean up/resetting test will be run in a separate file

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 8/21/2024
    Version: 1.0.0
"""
import sys
import logging
from Selenium_googleDriveTestUpload_Connection import (configure_keyring_googledrive, connect_googledrive,
                                                       configure_fortesting_googledrive, disconnect_googledrive)
from Selenium_googleDriveTestUpload_Files import create_file_newbutton, find_testfiles, validate_file_exists
from Selenium_googleDriveTestUpload_Folders import (create_folder_newbutton, get_folder_googledrive_id,
                                                    validate_folder_exists)
from Selenium_googleDriveTestUpload_Logging import start_logging

logger = logging.getLogger('seleniumTest.mainTest')  # main test logger


def execute_test(servicename: str, username: str, fldname: str):
    """
    Executes the following test steps*:
        - Open/log into Google Account
        - Open up Google Drive
        - Get test text file from the local ./testFiles folder
        - Create Google Drive folder "Testing Folder (Selenium)"
        - Validate the folder was created successfully (via Google API)
        - Upload file to Google Drive folder "Testing Folder (Selenium)"
        - Validate the file was uploaded successfully and return results to user
        - Close test
    *Clean up/resetting test will be run in a separate file

    :param servicename: Name used to securely store the appropriate Google Drive credentials in the keyring
    :type servicename: str
    :param username: Google Drive credential's username
    :type username: str
    :param fldname: Name of the test folder to be created
    :type fldname: str
    :return: A dictionary containing the {filename: folderID} if a success, if a failure, returns an empty dictionary
    :rtype: dict
    """
    continue_bool = ""
    dict_file = {}

    # Configure logging
    start_logging(filename="seleniumTestGoogleDriveUpload_mainTest.log")
    logger.info("----START: Beginning Selenium Google Drive Upload Test----")

    # Establish user creds (if needed)
    configure_keyring_googledrive(servicename=servicename, username=username)

    # Login to Google using creds
    chrome_options = configure_fortesting_googledrive()  # !--WARNING, SHOULD ONLY RUN THIS WITH A TEST ACCOUNT
    driver_chrome = connect_googledrive(servicename=servicename, username=username, chrome_options=chrome_options)

    # Create Google Drive folder
    create_folder_newbutton(fldname=fldname, driver=driver_chrome, navigate_to_googledrive=True)

    # Validate (with Google API) that the folder was created
    result_fld = validate_folder_exists(fldname=fldname)

    if result_fld is False:  # folder not created, stop test with failure
        logger.error(f"Folder '{fldname}' failed to be created in Google Drive.")
        continue_bool = False

    if continue_bool is not False:
        # Get folder ID (needed to navigate), and handle if there is more than one result
        fld_info = get_folder_googledrive_id(fldname=fldname)
        if (fld_info is None) or len(fld_info) < 1:
            logger.error(f"ERROR: Folder '{fldname}' does not exist, failed to be created.")
            continue_bool = False
        elif len(fld_info) > 1:
            logger.warning(f"More than one folder named '{fldname}' has been found. **Will use the most recent folder.**"
                           f"\nFolder list: {fld_info}")

            # Calc the newest folder and set fld_id to the id value for that record
            # {'id': 'IDvalue', 'createdTime': 'datetime', 'parents': 'parentID'}
            for fld in fld_info:
                if 'fld_id' not in locals():  # first time looping through, assign values
                    fld_id = fld['id']
                    fld_created = fld['createdTime']
                else:  # not first loop, compare to get most recent
                    if fld_created < fld['createdTime']:  # current record is older, assign newer values
                        fld_id = fld['id']
                        fld_created = fld['createdTime']
        else:  # only one result, set fld_id to the id value
            fld_id = fld_info[0]['id']
            fld_created = fld_info[0]['createdTime']

        if continue_bool is not False:
            logger.info(f"Folder info being used: folder ID '{fld_id}' and created time '{fld_created}'")

            # Get list of file(s) (.txt) to upload from local ./testFiles folder
            filetype = "txt"
            dict_test = find_testfiles(filetype=filetype)

            if not dict_test:  # no test files found
                logger.error(f"No files of type '.{filetype}' found, unable to test upload")
                continue_bool = False
            else:  # loop through and upload the files
                for key, value in dict_test.items():
                    create_file_newbutton(filename=key, filepath_abs=value, fld_uploadto_id=fld_id, driver=driver_chrome)
                    # validate that they were actually created
                    file_exists = validate_file_exists(filename=key, fld_id=fld_id)
                    if file_exists is True:
                        logger.info(f"SUCCESS: created file '{key}' in folder '{fld_id}'.")
                        dict_file[key] = fld_id  # add to the dict
                    else:
                        logger.error(
                            f"ERROR: Attempted to create file '{key}' in folder '{fld_id}', but unable to validate.")

    # Close test/driver
    disconnect_googledrive(driver_chrome)

    logger.info("----END: Selenium Google Drive Test Upload completed.----")

    return dict_file
