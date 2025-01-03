"""
SUMMARY: Executes all the unit tests in the local ./unitTests folder.  Running it this way because saving the
    unit tests in their own sub-folder adds an extra level of complexity.

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 8/22/2024
    Version: 1.0.0
"""

import unittest
import unitTests.test_Selenium_googleDriveTestUpload_Files as test_Selenium_googleDriveTest_Files
import unitTests.test_Selenium_googleDriveTestUpload_Folders as test_Selenium_googleDriveTest_Folders

# Load tests
suite_files = unittest.TestLoader().loadTestsFromModule(test_Selenium_googleDriveTest_Files)
suite_folders = unittest.TestLoader().loadTestsFromModule(test_Selenium_googleDriveTest_Folders)

# Execute tests
unittest.TextTestRunner(verbosity=2).run(suite_files)
unittest.TextTestRunner(verbosity=2).run(suite_folders)
