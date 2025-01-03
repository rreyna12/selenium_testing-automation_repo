"""
SUMMARY: Any modules related to opening a connection to Google Drive.  Such as using Selenium's WebDriver to open a
    Google Drive connection, or connecting with Google's API.

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 8/21/2024
    Version: 1.0.0
"""
import google.auth.exceptions
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import keyring  # must install: pip install keyring
import logging
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Selenium_googleDriveTestUpload_Logging import start_logging
from webdriver_manager.chrome import ChromeDriverManager


# Global variables
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly",  # permissions requested by the app
          "https://www.googleapis.com/auth/drive"]
# ***the cred_file is created when you configure OAuth connection via Google API, replace the file path below
cred_file = "---REPLACE-VALUE---"  # absolute file path
#cred_file = "C:/credentials_test.json"  # Window machines make sure to use front slashes
logger = logging.getLogger('seleniumTest.connection')  # connection logger


def configure_fortesting_googledrive():
    """
    Configure Google account to allow automation tester to connect
    !--WARNING: This can make your account MORE VULNERABLE TO HACKING, ONLY PERFORM THIS WITH A TEST ACCOUNT--!

    :return: A configuration of the chrome options needed for testing
    :rtype: Options
    """
    logger.info("Configuring google drive for testing")

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    return chrome_options


def configure_keyring_googledrive(servicename: str, username: str):
    """
    Configures a keyring to securely save account's Google Drive connection creds, if it doesn't already exist.  Allows
    the program to access and use these creds in the future.  For Windows machines, this saves the creds in your
    Credential Manager under Windows Credentials.

    :param servicename: Name of the service for which the creds are used, ex: "Google Drive"
    :type servicename: str
    :param username: Cred's username
    :type username: str
    """
    logger.info("Configuring keyring for google drive creds")

    if not (keyring.get_credential(servicename, username)):
        keyring.set_password(service_name=servicename, username=username, password=input("Password: "))

        logger.info("Keyring saved")
    else:
        logger.info("Keyring already exists, no action needed")


def connect_googledrive(servicename: str, username: str, chrome_options: Options()):
    """
    Connects to Google Drive via Selenium and a web browser

    :param servicename: Name of the service for which the creds are used, as saved in the keyring.
    :type servicename: str
    :param username: Cred's username, as saved in the keyring.
    :type username:
    :param chrome_options: Google Chrome configuration options
    :type chrome_options: Options

    :return: webdriver connection to chrome
    :rtype: webdriver
    """

    logger.info("Beginning connection to google")

    # Set the driver
    logger.debug("Setting the chrome driver")
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Open google website
    logger.debug("Open web browser")
    driver.get('https://www.google.com')

    # Maximize screen
    logger.debug("Maximize browser window size")
    driver.maximize_window()

    # Navigate to login Gmail
    logger.debug("Navigate to Google's login page")
    driver.get(
        "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&hl=en&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession")

    # Login - pass through test email
    logger.debug("Login process (email) - enter test email")
    driver.find_element(By.ID, "identifierId").send_keys(keyring.get_credential(servicename, username).username)

    # Login - click on 'Next' button and wait
    logger.debug("Login process (email) - click 'next' button")
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    driver.implicitly_wait(5)

    # Input password and click on 'Next'
    logger.debug("Login process (password) - enter password")
    input_pass = WebDriverWait(driver, 5).until(
        ec.element_to_be_clickable((By.XPATH, '//input[@name="Passwd"]')))
    input_pass.send_keys(keyring.get_password(servicename, username))
    driver.implicitly_wait(3)
    logger.debug("Login process (password) - click 'next' button")
    button_pass_next = WebDriverWait(driver, 5).until(
        ec.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    button_pass_next.click()
    driver.implicitly_wait(3)
    # Now logged in, navigate to google drive
    logger.debug("Navigate to google drive's home page")
    driver.get("https://drive.google.com/drive/home")
    driver.implicitly_wait(3)

    return driver


def disconnect_googledrive(driver: webdriver):
    """
    Closes the connection to the test driver

    :param driver: The webdriver to be closed
    :driver type: webdriver
    """
    logger.info("Closing connection to google chrome driver")

    driver.close()


def get_credentials_googledrive():
    """
    Configures user's credentials to connect to Google Drive via API

    :return: Google Drive credentials
    :rtype: Credentials
    """

    logger.info("Getting google drive login creds for Google's Drive API")

    creds = None
    # The file token.json stores the user's access and refresh tokens and is created automatically when the
    # authorization flow completes for the first time

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # attempt to refresh the creds, sometimes this fails so might need to reset them
        try:
            creds.refresh(Request())
        except google.auth.exceptions.RefreshError as error:
            # if refresh token fails, reset creds to none, will recreate below
            creds = None
            logger.warning(f"Unable to refresh OAuth creds required for Google API calls, resetting. Error: {error}")
            logger.error(error)

    # if there are no (valid) creds available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
            # save the creds for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    return creds

#----------------------
servicename = "Google Drive Test Account"
username = "testrreyna@gmail.com"
fld_test = "Testing Folder (Selenium)"

chrome_options = configure_fortesting_googledrive()  # !--WARNING, SHOULD ONLY RUN THIS WITH A TEST ACCOUNT
driver_chrome = connect_googledrive(servicename=servicename, username=username, chrome_options=chrome_options)
