"""
SUMMARY: Executes the test for Google Drive's Create folder and Upload file feature using Selenium, and then cleans
    up the test.

    TEST STEPS*:
        - Open/log into Google Account
        - Open up Google Drive
        - Get test text file from the local ./testFiles folder
        - Create Google Drive folder "Testing Folder (Selenium)"
        - Validate the folder was created successfully (via Google API)
        - Upload file to Google Drive folder "Testing Folder (Selenium)"
        - Validate the file was uploaded successfully and return results to user
        - Close test

    CLEAN UP STEPS: (done with Google API)
        - Find and delete Google Drive folder "Testing Folder (Selenium)" and all contents (file created)
        - Validate the folder and file no longer exist
        - Close test

NOTES:
    - See README.txt file for requirements to run and all sources used
    - keyring service account title and user name have been commented out for security reasons since I'm committing
        this to GitHub, will need to replace those values if running this script, replace ***** below in order to run
    - BEFORE RUNNING TEST, be sure to replace the following variables (placeholder, '---REPLACE-VALUE---'):
        1) servicename in Global Variables below
        2) username in Global Variables below
        3) cred_file in Selenium_googleDriveTestUpload_Connection file

VERSION INFO:
    Created by R. Reyna
    Date: 8/27/2024
    Version: 1.0.0
"""
from Selenium_googleDriveTestUpload_ExecuteTest import execute_test
from Selenium_googleDriveTestUpload_CleanUpTest import cleanup_test

# Global variables
servicename = "---REPLACE-VALUE---"
username = "---REPLACE-VALUE---"
fld_test = "Testing Folder (Selenium)"

dict_file_created = execute_test(servicename=servicename, username=username, fldname=fld_test)

if len(dict_file_created) > 0:  # only cleanup if the test successful; allows for troubleshooting w/items created
    print("SUCCESS: Test was a success, beginning cleanup")
    for key, value in dict_file_created.items():
        cleanup_test(servicename=servicename, username=username, fldname=fld_test, filename=key)
else:
    print("WARNING: test was not successful, not executing clean up steps")
