Personal project(s) to learn how to use Selenium, an open source test automation tool.

# <ins>Table of Contents</ins>:
1. [First Project (Selenium Site Walkthrough)](#first-project)
2. [Selenium / Google Drive Test - Upload File and Clean Up](#gdrive-upload-file)

# <ins>PROJECTS</ins>:
## firstProject_SeleniumSiteWalkthrough <a name="first-project"></a>
**<ins>Summary</ins>:** Simple first Selenium WebDriver & python project per walk through steps on Selenium's site https://www.selenium.dev/documentation/webdriver/getting_started/. It executes a search on Amazon and validates the results.

**<ins>Steps</ins>:**
  1. Navigate to Amazon
  2. Search for item
  3. Wait
  4. Validate search results

**<ins>Pre reqs</ins>:** 
  - Install Selenium `pip install Selenium`

    *If using Pycharm, additional step needed to install Selenium package:*
       - *click on Python version in bottom right corner*
       - *select Interpreter Setting*
       - *select Python Interpretor*
  - If needed, install browser plug-ins to help determine web object names
      - I used Chrome's Inspect and CSS Selector

**<ins>Notes</ins>:**
This test will fail if run too frequently, as Amazon's "validate you're not a robot" page will come up

**<ins>How to run</ins>:**
  1. Download the `firstPRoject_SeleniumSiteWalkthrough` folder
  2. Complete the pre req steps above
  3. Execute the `Selenium_firstProject.py` file

## test_googleDrive_Upload-and-Cleanup <a name="gdrive-upload-file"></a>
**<ins>Summary</ins>:** A more robust Selenium WebDriver & python project that, with a test account, creates a folder in Google Drive and uploads a test document.  It then validates the results and if successful, logs the output and then cleans up the test.  If unsuccessful, logs output to the user for troubleshooting.

Includes custom native python functions as needed and unit testing for those functions.

**<ins>Steps (Testing)</ins>:**
  1. Establish user credentials for Google Drive (if needed) and securely save to keyring
  2. Open web browser (Chrome) and navigate to Google's account login page
  3. Log into Google Account using creds saved to keyring
  4. Navigate to Google Drive
  5. Get test .txt file from the local ./testFiles folder
  6. Create Google Drive folder "Testing Folder (Selenium)" _(will create even if other previous testing folders still exist)_
  7. Validate the folder was created successfully (via Google API)
  8. Upload file to Google Drive folder "Testing Folder (Selenium)" _(if multiple folders exist, will use most recent)_
  9. Validate the file was uploaded successfully (via Google API) and return results to user
  10. Close test

**<ins>Steps (Clean up)</ins>:**
  *clean up is done with Google API*
  1. Determines a list of all instances of Google Drive folder "Testing Folder (Selenium)" to delete _(in case previous clean ups failed)_
  2. Loops through list and deletes the instance(s)
  3. Validates the deletion was successful and the folder and file no longer exist
  4. Close test

**<ins>Pre reqs</ins>:**   
- *If using Pycharm, additional steps needed to install packages below:*
  - *click on Python version in bottom right corner*
  - *select Interpreter Setting*
  - *select Python Interpretor*
  - *select Install button (+) and find the package*
    
- Install the folowing - pip installation command listed below, as well as the interpreter names to install if different from package name:
    - <ins>Selenium</ins>: _for automating web clicks_

      `pip install Selenium`
      `pip install webdriver-manager`
    - <ins>Keyring</ins>: _for safely storing Google Drive Creds.  Note, creds stored by keyring can also be accessed by the Windows Credential Manager, which applies additional security to the creds, only allowing approved
users to view the password or change the record._

      `pip install keyring`
    - <ins>Google API</ins>: _used to speed up the test by helping validate, get object IDs and delete/clean up Google Drive objects_
      
      `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

      Python Interpreter Names:
        - Google API (google-api-core and google-api-python-client)
        - Google Auth (google-auth and google-auth-oauthlib)
    - <ins>Pyperclip</ins>: _allows us to copy from code to the clipboard https://pypi.org/project/pyperclip/_

      `pip install pyperclip`
    - <ins>PyAutoGUI</ins>: _allows use of hot keys from code (ex: ctrl+v combo) https://pyautogui.readthedocs.io/en/latest/_

      `pip install pyautogui`
- Configure your Google Drive test account* to work with Google Drive API, including installing Google API client and Google OAuth libraries (*see warning below)
  - https://www.geeksforgeeks.org/upload-and-download-files-from-google-drive-storage-using-python/
  - https://stackoverflow.com/questions/75454425/access-blocked-project-has-not-completed-the-google-verification-process 
- If needed, install browser plug-ins, I've listed what I used below
  - to help determine web object names: Chrome's Inspect and CSS Selector
  - XPath extensions: SelectorsHub

**<ins>Notes</ins>:**
To view a list of sources used to complete the project, see the `Sources.txt` file.

**!--WARNING--!**
Google drive login: to do this with an automated tested you must enable less secure apps to access your account and !!!-can make your account more vulnerable to hacking - **TEST WITH AN EXTRA ACCOUNT ONLY, DO NOT USE ON PRIMARY ACCOUNT**-!!!
For this test I have created a test google account.

<ins>Topics covered</ins>:
- <ins>Selenium & Python</ins>: using selenium with python to automate user actions (web clicks) on the Google Drive site
    - identifying and calling web objects via CSS
    - managing sub-menus and drop downs
    - interacting with windows explorer pop ups from Google Drive
 - <ins>Python & Unit Tests</ins>: Creating python unit tests to help maintain non-Selenium functions
 - <ins>Python & Google API</ins>: using google API and python to validate test steps and manage google drive as needed (ex: validating files were created, deleting files and folders, getting google object ID's)
 - <ins>Python & Logging</ins>: Creating and managing helpful log files
 - <ins>Keyring</ins>: securely saving creds on a windows machine

**<ins>How to run</ins>:**

**Execute Full Test:**
  1. Download the `test_googleDrive_Upload-and-Cleanup` folder
  2. **REPLACE THE FOLLOWING VARIABLES** in the `Selenium_googleDriveTestUpload_ExecuteFULL_Test-and-Cleanup.py` file
      + servicename in Global Variables
      + username in Global Variables
      + cred_file in `Selenium_googleDriveTestUpload_Connection` file
  3. Complete the pre req steps listed above
  4. Execute the `Selenium_googleDriveTestUpload_ExecuteFULL_Test-and-Cleanup.py` file
     
**Execute Specific Parts of the Test:**
  + Unit Tests *(the tests themselves are stored in the `./unitTests` folder)*
      1. Complete steps 1 & 3 of the full test execution steps above
      2. Execute the `Test_Selenium_googleDriveTestUpload_ExecuteUnitTests.py` file
  + Selenium / Google Drive Test
      1. Complete steps 1-3 of the full test execution steps above
      2. Execute the `Selenium_googleDriveTestUpload_ExecuteTest.py` file
  + Clean Up
      1. Complete steps 1-3 of the full test execution steps above
      2. Execute the `Selenium_googleDriveTestUpload_CleanUpTest.py` file

**Troubleshooting:**

Log file will be created named "seleniumTestGoogleDriveUpload_mainTest.log"
+ beginning of each portion of the test (main test and clean up) will be noted by `----START:` in the log file
+ ending of each portion of the test (main test and clean up) will be noted by `----END:` in the log file

<ins>Common Issue(s)</ins>:

ISSUE: Program won't log into Google Account, despite successfully pasting in the email and password.  The Sign In page is brought again up after attempting to log in and the test doesn't continue.
  + FIX: Google does have protections against using automation accounts.  While the test will run successfully, I found during testing that if I execute it too many times, it would start doing the issue listed above.  Taking a break and coming back and re-running it later would fix the issue.
