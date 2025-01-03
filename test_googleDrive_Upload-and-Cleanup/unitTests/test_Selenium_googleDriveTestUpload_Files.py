"""
Summary: Will test functions in Selenium_googleDriveTest_Upload_Files module that have expected python results (not
    Selenium)

SOURCES:
    - unit tests: https://www.freecodecamp.org/news/how-to-write-unit-tests-for-python-functions/

VERSION INFO:
    Created by R. Reyna
    Date: 8/22/2024
    Version: 1.0.0
"""

import os
from Selenium_googleDriveTestUpload_Files import find_testfiles, replace_backslash, validate_file_exists
import unittest


class TestClass(unittest.TestCase):

    def test_find_testfiles_filetype_txt(self):
        """Tests find_testfiles function for a single file type (.txt), quantity all"""
        dict_files = find_testfiles(filetype="txt")
        if not bool(dict_files):  # check to see if dictionary is empty
            self.fail(msg="FAIL: Expected .txt file results, but no .txt files found")
        else:
            for filename in dict_files.keys():
                if filename.find(".txt") == -1:
                    self.fail(msg="FAIL: Expected .txt file results, but no .txt files found")

    def test_find_testfiles_filetype_csv(self):
        """Tests find_testfiles function for a single file type (.csv), quantity all"""
        dict_files = find_testfiles(filetype="csv")
        if not bool(dict_files):  # check to see if dictionary is empty
            self.fail(msg="FAIL: Expected .csv file results, but no .csv files found")
        else:
            for filename in dict_files.keys():
                if filename.find(".csv") == -1:
                    self.fail(msg="FAIL: Expected .csv file results, but no .csv files found")

    def test_find_testfiles_filetype_default(self):
        """Tests find_testfiles function with no file type provided, meaning all file types should be returned, and
        folders should be excluded from results, quantity all"""
        dict_files = find_testfiles()
        if not bool(dict_files):  # check to see if dictionary is empty
            self.fail(msg="FAIL: Expected file(s), but no files found.")
        else:
            for filepath in dict_files.values():
                if os.path.isdir(filepath):
                    self.fail(msg="FAIL: Expected file(s), but no files found.")

    def test_replace_backslash_filepath_frontslash(self):
        """Tests the replace_backslash_single function against a file path that uses only front slashes"""

        self.assertEqual(replace_backslash(
            "C:\\Users\\maiko\\GitRepos\\selenium_testing-automation_repo\\test_googleDrive_Upload-and-Cleanup"),
            "C:/Users/maiko/GitRepos/selenium_testing-automation_repo/test_googleDrive_Upload-and-Cleanup")

    def test_replace_backslash_filepath_backslash(self):
        """Tests the replace_backslash_single function against a file path that uses only backslashes"""

        self.assertEqual(replace_backslash("C:/Users/maiko/GitRepos/selenium_testing-automation_repo/"
                                           "test_googleDrive_Upload-and-Cleanup"),
                         "C:/Users/maiko/GitRepos/selenium_testing-automation_repo/"
                         "test_googleDrive_Upload-and-Cleanup")

    def test_replace_backslash_filepath_frontslashandbackslash(self):
        """Tests the replace_backslash_single function against a file path that has a mix of front and backslashes"""

        self.assertEqual(replace_backslash("C:/Users/maiko/GitRepos/selenium_testing-automation_repo/"
                                           "test_googleDrive_Upload-and-Cleanup\\TestFile_googleDriveTestUpload-1.txt"),
                         "C:/Users/maiko/GitRepos/selenium_testing-automation_repo/"
                         "test_googleDrive_Upload-and-Cleanup/TestFile_googleDriveTestUpload-1.txt")

    def validate_file_exists_by_name(self):
        """Tests the validate_file_exists function against a test folder and file that *should* exist
                in the test Google Drive account by name only, no folder ID.
                ***Relies on file 'DoNotDelete-TestFile-1.txt' existing in the test account (should be in folder
                'Do not delete - test folder', ID '1qCaESsPJ3kp27g39xGEPPVei-gnX73D4')"""

        self.assertTrue(validate_file_exists_by_name_folder(filename="DoNotDelete-TestFile-1.txt"))

    def validate_file_exists_by_name_folder(self):
        """Tests the validate_file_exists function against a test folder and file that *should* exist
        in the test google drive account by using both name and folder ID.
        ***Relies on folder 'Do not delete - test folder', ID '1qCaESsPJ3kp27g39xGEPPVei-gnX73D4' and file
        'DoNotDelete-TestFile-1.txt' existing in the test account***"""

        self.assertTrue(validate_file_exists_by_name_folder(filename="DoNotDelete-TestFile-1.txt"
                                                            , fld_id="1qCaESsPJ3kp27g39xGEPPVei-gnX73D4"))

    def test_validate_file_exists_Error(self):
        """Tests validate_file_exists function for a folder that does exist, however, neither required parameter (name,
        id) have been provided so the function should throw an error"""
        with self.assertRaises(SystemExit):
            validate_file_exists()


if __name__ == '__main__':
    unittest.main()
