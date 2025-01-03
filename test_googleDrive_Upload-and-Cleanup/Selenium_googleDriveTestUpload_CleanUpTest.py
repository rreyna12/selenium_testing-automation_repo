"""
SUMMARY: Cleans up all actions taken in the Selenium test for Google Drive's Create folder
    and Upload file feature.  This clean up allows the test to be re-run.

    CLEAN UP STEPS*:
        - Determine a list of all instances of Google Drive folder "Testing Folder (Selenium)" to delete (in case
            previous clean ups failed)
        - Loops through list and deletes the instance(s)
        - Validate the deletion was successful and folder(s) and file(s) no longer exist
        - Close test

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 8/22/2024
    Version: 1.0.0
"""
import logging
from Selenium_googleDriveTestUpload_Logging import start_logging
from Selenium_googleDriveTestUpload_Files import (get_file_googledrive_id, delete_file_googledrive_by_id,
                                                  validate_file_exists)
from Selenium_googleDriveTestUpload_Folders import delete_folder_googledrive_by_id, get_folder_googledrive_id

logger = logging.getLogger('seleniumTest.cleanUp')  # clean up logger


def cleanup_test(servicename: str, username: str, fldname: str, filename: str):
    """
    Cleans up any files/folders that were created as part of the Selenium Google Drive Upload test.
    Folders - deletes *ALL* folders with the specified folder name < this ensures that all test folders are cleaned up,
        even if the previous test clean up failed
    Files - the file should be deleted as part of the folder deletion, however, because the name of the file is unique
        to this test, the function will also validate that after the folder deletion, if there are any files with the
        specified name, they are --also deleted--.  This ensures that if there is an error during testing and a file
        is incorrectly uploaded, it is still cleaned up.

    Clean up is done via Google API to speed things up, not Selenium

    :param servicename:
    :param username:
    :param fldname: Name of the folder(s) to be cleaned up
    :type fldname: str
    :param filename: Name of the file(s) to be cleaned up
    :type filename: str
    :return:
    """

    # Configure logging
    start_logging(filename="seleniumTestGoogleDriveUpload_cleanUp.log")

    # Get list of folder(s) to clean up & delete
    fld_info = get_folder_googledrive_id(fldname=fldname)
    if (fld_info is None) or len(fld_info) < 1:
        logger.warning(f"Unable to find '{fldname}'; will not take any clean up actions.")
    else:
        if len(fld_info) > 1:
            logger.warning(f"More than one instance of '{fldname}' found, will delete ALL instances."
                           f"\nFolder list: {fld_info}")
        else:
            logger.info(f"Only one instance of '{fldname}' found, cleaning up")

        # Delete folders
        for fld in fld_info:
            logger.debug(f"Folder deletion for ID '{fld['id']}': Attempting deletion")
            result = delete_folder_googledrive_by_id(fld_id=fld['id'])

            # Validate if deletion was successful
            if result is True:
                logger.debug(f"Folder deletion for ID '{fld['id']}': SUCCESS")
            else:
                logger.error(f"Folder deletion for ID '{fld['id']}': FAILURE")

    # Validate that there are no longer any files with the name provided
    file_exists = validate_file_exists(filename=filename)
    if file_exists:  # files found, possibly from other tests, delete
        logger.warning(f"Test file should have been cleaned up with folder deletion, however, copies of '{filename}'"
                       f"were still found.  Will attempt to clean up.")
        # Get file ID, and handle if there is more than one result
        file_info = get_file_googledrive_id(filename=filename)
        if (file_info is None) or len(file_info) < 1:
            logger.error(f"ERROR: validate_file_exists states that '{filename}' exists, however, unable to get file ID "
                          f"in order to delete. Will not take any clean up actions.")
        else:
            if len(file_info > 1):
                logger.warning(f"More than one extra instance of '{filename}' found, will delete ALL instances."
                               f"\nFile list: {file_info}")
            else:
                logger.info(f"Only one extra instance of '{filename}' found, cleaning up.")

                # Delete files
                for file in file_info:
                    logger.debug(f"File deletion for ID '{file['id']}' in folder ID '{file['parents']}': Attempting deletion")
                    result = delete_file_googledrive_by_id(file_id=file['id'])

                    # Validate if deletion was successful
                    if result is True:
                        logger.debug(f"File deletion for ID '{file['id']}' in folder ID '{file['parents']}': SUCCESS")
                    else:
                        logger.error(f"File deletion for ID '{file['id']}' in folder ID '{file['parents']}': FAILURE")

    logger.info("Test clean up complete.")
