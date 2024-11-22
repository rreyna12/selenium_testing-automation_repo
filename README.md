Personal project(s) to learn how to use Selenium, an open source test automation tool.

# <ins>PROJECTS</ins>:
## firstProject_SeleniumSiteWalkthrough
**<ins>Summary</ins>:** Simple first Selenium/python project per walk through steps on Selenium's site https://www.selenium.dev/documentation/webdriver/getting_started/. It executes a search on Amazon and validates the results.

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
  1. Download the firstPRoject_SeleniumSiteWalkthrough folder
  2. Complete the pre req steps above
  3. Execute the `Selenium_firstProject.py` file

## test_googleDrive_Upload-and-Cleanup
**<ins>Summary</ins>:** A more robust Selenium/python project that, with a test account, creates a folder in Google Drive and uploads a test document.  It then validates the results and if successful, logs the output and then cleans up the test.  If unsuccessful, logs output to the user for troubleshooting.

Includes native python functions as needed and unit testing for those functions.

**<ins>Steps (Testing)</ins>:**
  1. Open/log into Google Account
  2. Open up Google Drive
  3. Get test text file from the local ./testFiles folder
  4. Create Google Drive folder "Testing Folder (Selenium)"
  5. Validate the folder was created successfully (via Google API)
  6. Upload file to Google Drive folder "Testing Folder (Selenium)"
  7. Validate the file was uploaded successfully and return results to user
  8. Close test

**<ins>Steps (Clean up)</ins>:**
  1. Open/log into Google Account
  2. Open up Google Drive
  3. Find and delete Google Drive folder "Testing Folder (Selenium)" and all contents (file created)
  4. Validate the folder and file no longer exist
  5. Close test

**<ins>Pre reqs</ins>:** 
    *If using Pycharm, additional steps needed to install packages below:*
       - *click on Python version in bottom right corner*
       - *select Interpreter Setting*
       - *select Python Interpretor*
       - *select Install button (+) and find the package*
  - Install Selenium `pip install Selenium`
  - If needed, install browser plug-ins to help determine web object names
      - I used Chrome's Inspect and CSS Selector

**<ins>Notes</ins>:**


**<ins>How to run</ins>:**
  1. **REPLACE THE FOLLOWING VARIABLES** in the `Selenium_googleDriveTestUpload_ExecuteFULL_Test-and-Cleanup.py` file
      + servicename in Global Variables
      + username in Global Variables
      + cred_file in `Selenium_googleDriveTestUpload_Connection` file
  3. t
