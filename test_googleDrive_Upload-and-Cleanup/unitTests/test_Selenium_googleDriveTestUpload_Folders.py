"""
Summary: Will test functions in Selenium_googleDriveTest_Folders module that have expected python results (not
    Selenium)

SOURCES:
    - unit tests: https://www.freecodecamp.org/news/how-to-write-unit-tests-for-python-functions/

VERSION INFO:
    Created by R. Reyna
    Date: 9/5/2024
    Version: 1.0.0
"""
from Selenium_googleDriveTestUpload_Folders import get_folder_googledrive_id, validate_folder_exists
import sys
import unittest


class TestClass(unittest.TestCase):

    def test_get_folder_googledrive_id_empty_result(self):
        """Tests get_folder_googledrive_id for a folder that doesn't exist, expects None as a result"""
        fldname = "this folder does not exist and never will"
        result = get_folder_googledrive_id(fldname=fldname)
        if result is not None:
            self.fail(f"FAIL: Expected None as a result for '{fldname}', instead found {len(result)}")

    def test_get_folder_googledrive_id_one_result(self):
        """Tests get_folder_googledrive_id for a folder that should only have one result"""
        fldname = "DO NOT DELETE - used for unit test"
        result = get_folder_googledrive_id(fldname=fldname)
        if len(result) is not 1:
            self.fail(msg=f"FAIL: Expected 1 result for '{fldname}', instead found {len(result)}")

    def test_get_folder_googledrive_id_multi_result(self):
        """Tests get_folder_googledrive_id for a folder that should have multiple results"""
        fldname = "Do not delete - test folder"
        result = get_folder_googledrive_id(fldname=fldname)
        if len(result) < 2:
            self.fail(msg=f"FAIL: Expected 2 results for '{fldname}', instead found {len(result)}")

        print("just need this line to make break")

    def test_validate_folder_exists_by_id_True(self):
        """Tests validate_folder function for a folder that does exist, by ID"""
        fld_id_req = "1YszOGXw70BfXqmMBTBHNvSh_WrawOYl0"  # folder name: "DO NOT DELETE - used for unit test"
        result = validate_folder_exists(fld_id=fld_id_req)
        self.assertTrue(expr=result, msg=f"FAIL: Expected '{fld_id_req}' to exist.")

    def test_validate_folder_exists_by_id_False(self):
        """Tests validate_folder function for a folder that does exist, by ID"""
        fld_id = "abcd1234"
        result = validate_folder_exists(fld_id=fld_id)
        self.assertFalse(expr=result, msg=f"FAIL: Expected '{fld_id}' to not exist.")

    def test_validate_folder_exists_by_name_True(self):
        """Tests validate_folder function for a folder that does exist, by name"""
        fld_test_req = "DO NOT DELETE - used for unit test"
        result = validate_folder_exists(fldname=fld_test_req)
        self.assertTrue(expr=result, msg=f"FAIL: Expected '{fld_test_req}' to exist.")

    def test_validate_folder_exists_by_name_False(self):
        """Tests validate_folder function for a folder that does exist, by name"""
        fldname = "this folder will never be created"
        result = validate_folder_exists(fldname=fldname)
        self.assertFalse(expr=result, msg=f"FAIL: Expected '{fldname}' to not exist.")

    def test_validate_folder_exists_Error(self):
        """Tests validate_folder_exists function for a folder that does exist, however, neither required parameter
        (name, id) have been provided so the function should throw an error"""
        with self.assertRaises(SystemExit):
            validate_folder_exists()


if __name__ == '__main__':
    unittest.main()