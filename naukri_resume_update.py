import logging
import logging.config
import os
import sys
import time

import requests
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
# ROOT_DIR = ""

logging.config.fileConfig("logging_config.ini")
run_every_secs = int(os.environ.get("RUN_EVERY_SECS", 10))


def schedule_run(run_every_secs):
    """Decorator to schedule a function run every specified seconds"""
    def schedule(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            s = time.time()
            while True:
                if time.time()-s > run_every_secs:
                    res = func(*args, **kwargs)
                    print(f"Time taken - {time.time()-s}")
                    s = time.time()

                time.sleep(5)

            return res

        return wrapper

    return schedule


def get_resume_path():
    """Downloads resume from pdf url specified in environment variable `RESUME_PDF_URL`"""
    url = os.environ.get("RESUME_PDF_URL")

    resume_file_path = os.path.abspath(os.path.join(
        ROOT_DIR, "kartikey_porwal_resume.pdf"))

    with open(resume_file_path, "wb") as f:
        with requests.get(url) as res:
            f.write(res.content)

    return resume_file_path


class NaukriLogin(object):
    def __init__(self, username, password):
        """Initialises webdriver and opens the login page
        Arguments:
            username {str} -- email of the naukri user
            password {str} -- password of the naukri user
        """
        self.logger = logging.getLogger()

        self._profile_url = r"https://www.naukri.com/mnjuser/profile"

        if os.environ.get("WEBDRIVER_MODE", "CHROME") == "CHROME":
            self.initiate_chrome_webdriver
        else:
            self.initiate_firefox_webdriver

        self.logger.info(f"Initialized the webdriver")

        self.driver.maximize_window()
        self.logger.info("Driver window maximized.")

        self.driver.get(r"https://www.naukri.com/nlogin/login")
        self.logger.debug("opening Naukri.")

        self.username = username
        self.password = password
        # self.driver.save_screenshot("p.png")

    @property
    def initiate_chrome_webdriver(self):
        """Initiates a driver instance of chrome webdriver"""

        self.logger.info(f"Initializing chrome driver")
        try:
            # instantiate chrome webdriver
            self._chrome_options = webdriver.ChromeOptions()

            # open in incognito mode
            self._chrome_options.add_argument("-incognito")

            self._chrome_options.binary_location = os.environ.get(
                "GOOGLE_CHROME_BIN")

            # # open chrome without gui
            self._chrome_options.add_argument("--headless")

            # This disables the message "Chrome is being is controlled by automated test software."
            # # deprecated in newer version of chrome webdriver
            # self._chrome_options.add_argument("disable-infobars")
            # this one works
            self._chrome_options.add_experimental_option(
                name="excludeSwitches",
                value=['enable-automation']
            )
            self._chrome_options.add_experimental_option("detach", True)

            # # set user agent
            # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36
            # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/77.0.3865.90 Safari/537.36
            self._chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")

            self._chrome_options.add_argument("--disable-popups")
            self._chrome_options.add_argument("--disable-notifications")
            self._chrome_options.add_argument("--disable-gpu")
            self._chrome_options.add_argument("--no-sandbox")
            self._chrome_options.add_argument("--disable-dev-sh-usage")

            self.driver = webdriver.Chrome(
                executable_path=os.environ.get("CHROME_WEBDRIVER_PATH"),
                # executable_path=ChromeDriverManager().install(),
                options=self._chrome_options,
            )

            # get user agent
            agent = self.driver.execute_script("return navigator.userAgent")
            self.logger.info(
                f"Chrome Driver initiated with user agent: {agent}")

        except Exception as e:
            self.logger.exception(
                f'Error when initializing chrome driver on line {sys.exc_info()[-1].tb_lineno} Error Name: {type(e).__name__} Error: {e}')

            raise e

    @property
    def initiate_firefox_webdriver(self):
        """Initiates a driver instance of firefox webdriver"""

        self.logger.info(f"Initializing gecko driver")
        try:
            # instantiating firefox webdriver
            self._firefox_options = webdriver.FirefoxOptions()
            # open in incognito mode
            self._firefox_options.add_argument("-incognito")

            # open chrome without gui
            self._firefox_options.add_argument("--headless")

            self._firefox_options.add_argument("--disable-popups")
            self._firefox_options.add_argument("--disable-notifications")
            self._firefox_options.add_argument("--disable-gpu")
            self._firefox_options.add_argument("--no-sandbox")
            self._firefox_options.add_argument("--disable-dev-sh-usage")

            # setting user agent for firefox profile
            self._firefox_profile = webdriver.FirefoxProfile()

            # set user agent
            # Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
            # Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
            self._firefox_profile.set_preference(
                key="general.useragent.override",
                value="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            )

            self.driver = webdriver.Firefox(
                firefox_binary=os.environ.get("FIREFOX_BINARY_PATH"),
                executable_path=os.environ.get("GECKO_WEBDRIVER_PATH"),
                options=self._firefox_options,
                firefox_profile=self._firefox_profile,
                # service_log_path=os.path.devnull,
                # service_log_path=os.path.join(ROOT_DIR, "geckodriver.log"),
            )

            # get user agent
            agent = self.driver.execute_script("return navigator.userAgent")
            self.logger.info(
                f"Firefox Driver initiated with user agent: {agent}")
        except Exception as e:
            self.logger.exception(
                f'Error when initializing geckodriver on line {sys.exc_info()[-1].tb_lineno} Error Name: {type(e).__name__} Error: {e}')

            raise e

    # Login to naukri account

    def login(self):
        """Logs in to the naukri account using specified credentials and follows the users afterwards"""
        username_elem_id = "usernameField"
        password_elem_id = "passwordField"

        while 'naukri.com' not in self.driver.title.lower():
            print(f"Waiting for page to load")

        try:
            # ----------------------------------------------------------------------------------------
            # Finding, entering and clicking on email form found on login page
            try:
                self.logger.debug("Finding username element by id:  email ")
                self._email = self.driver.find_element_by_id(username_elem_id)
                self._email.send_keys(self.username)
                self.logger.debug(
                    f"Element Found: {self._email} Entered email/username: {self.username} ")
            except:
                self.logger.exception("Error found in finding email link:  ")
                self.logger.debug(
                    "Finding email/username element using explicit time by id:  email. ")
                self._email = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, username_elem_id))
                )
                self._email.send_keys(self.username)
                self.logger.debug(
                    f"Element Found: {self._email} Entered email: {self.username}  ")

            time.sleep(2)
            # ----------------------------------------------------------------------------------------
            # finding password element by id
            try:
                self.logger.debug(
                    f"Finding password element by id:  {password_elem_id}")
                self._pas = self.driver.find_element_by_id(password_elem_id)
                self._pas.send_keys(self.password + Keys.ENTER)
                self.logger.debug(
                    f"Password Element Found: {self._pas} Pressed enter. ")
            except:
                self.logger.exception(
                    "Error found in finding password link:  ")

                # wait for transition then continue to fill items
                self.logger.debug(
                    f"Finding password element by name with explicit wait - id: {password_elem_id} ")
                self._pas = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, password_elem_id)))
                self._pas.send_keys(self.password, Keys.ENTER)

                self.logger.debug(f"Password Element Found: {self._pas} ")

            # ----------------------------------------------------------------------------------------

        except:
            self.new_ui_login

        time.sleep(5)

        # self.driver.quit()

    @property
    def new_ui_login(self):
        username_elem_name = "usernameField"
        password_elem_name = "passwordField"

        # ----------------------------------------------------------------------------------------
        # finding email element from new naukri login page by name
        try:
            self.logger.info("Finding email element from new UI")
            self._email = self.driver.find_element_by_name(
                name=username_elem_name
            )
            self._email.send_keys(self.username)
            self.logger.debug(
                f"Element Found: {self._email}. Entered email/username: {self.username}")

        except Exception:
            self.logger.exception("Error found in finding email link:  ")
            self.logger.debug(
                "Finding email/username element using explicit time by name:  email")
            self._email = WebDriverWait(
                driver=self.driver,
                timeout=30
            ).until(
                EC.presence_of_element_located(
                    locator=(By.NAME, username_elem_name)
                )
            )
            self._email.send_keys(self.username)
            self.logger.debug(
                f"Element Found: {self._email}. Entered email: {self.username}")

        # ----------------------------------------------------------------------------------------
        # finding password element from new naukri login page by name
        try:
            self.logger.info("Finding password element from new UI")
            self._pas = self.driver.find_element_by_name(
                name=password_elem_name
            )
            self._pas.send_keys(self.password + Keys.ENTER)
            self.logger.debug(
                f"Element Found: {self._pas}.")

        except Exception:
            self.logger.exception("Error found in finding password link:  ")
            self.logger.debug(
                f"Finding password element using explicit time by name:  {password_elem_name}")
            self._pas = WebDriverWait(
                driver=self.driver,
                timeout=30
            ).until(
                EC.presence_of_element_located(
                    locator=(By.NAME, password_elem_name)
                )
            )
            self._pas.send_keys(self.password+Keys.ENTER)
            self.logger.debug(
                f"Element Found: {self._pas}")

    # update resume
    def update_resume(self):
        try:
            time.sleep(30)
            resume_file_path = get_resume_path()
            self.logger.info(
                f"Retrieved resume file path - {resume_file_path}")

            # self.driver.refresh()
            self.driver.get(self._profile_url)
            time.sleep(60)

            resume_class = "right download"
            upload_resume_id = "attachCV"
            resume_class = upload_resume_id

            resume_submit_button_xpath = "//input[@type='button' and @value='Update Resume']"
            resume_submit_button_xpath = "//input[@type='button']"
            # resume_submit_button_xpath = "//button[@type='button']"
            # resume_submit_button_xpath = "result"
            # resume_submit_button_xpath = "btn btn-block dummyUpload fs14"
            # resume_submit_button_xpath = ".btn.btn-block.dummyUpload.fs14"

            # last_height = self.driver.execute_script("return document.body.scrollHeight")
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            # ----------------------------------------------------------------------------------------
            # finding resume element from naukri profile
            try:
                self.logger.info(f"Finding resume element - {resume_class}")
                self._resume_elem = self.driver.find_element_by_id(
                    id_=resume_class)
                self._resume_elem.send_keys(resume_file_path)
                self.logger.debug(
                    f"Element Found: {self._resume_elem}. ")

            except Exception:
                self.logger.exception(
                    "Error found in finding resume element:  ")
                self.logger.debug(
                    f"Finding resume element using explicit time:  {resume_class}")
                self._resume_elem = WebDriverWait(
                    driver=self.driver,
                    timeout=30
                ).until(
                    EC.presence_of_element_located(
                        locator=(By.ID, resume_class)
                    )
                )
                self._resume_elem.send_keys(resume_file_path)

                self.logger.debug(
                    f"Element Found: {self._resume_elem}. ")

            # ----------------------------------------------------------------------------------------
            # finding resume submit button
            try:
                self.logger.info(
                    f"Finding resume submit button element - {resume_submit_button_xpath}")
                self._resume_submit_elem = self.driver.find_element_by_xpath(
                    resume_submit_button_xpath)
                self._resume_submit_elem.send_keys(Keys.RETURN)
                # self._resume_submit_elem.click()
                # self.driver.execute_script("arguments[0].click();", self._resume_submit_elem)

                # a = ActionChains(self.driver).move_to_element(self._resume_submit_elem)
                # a.click().perform()

                self.logger.debug(
                    f"Element Found: {self._resume_submit_elem}. Button Pressed")

            except Exception:
                self.logger.exception(
                    "Error found in finding resume submit button element:  ")
                self.logger.debug(
                    f"Finding resume submit button element using explicit time:  {resume_submit_button_xpath}")
                self._resume_submit_elem = WebDriverWait(
                    driver=self.driver,
                    timeout=30
                ).until(
                    EC.presence_of_element_located(
                        locator=(By.XPATH, resume_submit_button_xpath)
                    )
                )
                self._resume_submit_elem.send_keys(Keys.RETURN)

                # self._resume_submit_elem.click()
                # self.driver.execute_script("arguments[0].click();", self._resume_submit_elem)
                # ActionChains(self.driver).move_to_element(self._resume_submit_elem).click().perform()

                self.logger.debug(
                    f"Element Found: {self._resume_submit_elem}. Button Pressed")

        except Exception as e:
            self.logger.error(
                f'Will try next time. Unexpected error occurred at line {sys.exc_info()[-1].tb_lineno} Error Name: {type(e).__name__} Error: {e}')


@schedule_run(run_every_secs=run_every_secs)
def main():
    try:
        naukri = NaukriLogin(username=os.environ.get("NAUKRI_USER_EMAIL"),
                             password=os.environ.get("NAUKRI_USER_PASSWORD"),
                             )
        print("Login to naukri.com")
        naukri.login()

        print(f"Updating resume")
        naukri.update_resume()

    except Exception as e:
        print(
            f'Error on line {sys.exc_info()[-1].tb_lineno} Error Name: {type(e).__name__} Error: {e}')

    finally:
        time.sleep(5)
        if naukri.driver.service.process != None:
            naukri.driver.quit()


if __name__ == "__main__":

    print(f"Instantiating the script")

    firefox_binary = os.environ.get("FIREFOX_BINARY_PATH")
    executable_path = os.environ.get("GECKO_WEBDRIVER_PATH")

    chrome_binary = os.environ.get("GOOGLE_CHROME_BIN")
    chromedriver_path = os.environ.get("CHROME_WEBDRIVER_PATH")

    print(
        f"Firefox binary - {firefox_binary} exists - {os.path.isfile(firefox_binary)} and executable - {os.access(firefox_binary, os.X_OK)}")
    print(
        f"Geckodriver binary - {executable_path} exists - {os.path.isfile(executable_path)} and executable - {os.access(executable_path, os.X_OK)}")

    print(
        f"Chrome binary - {chrome_binary} exists - {os.path.isfile(chrome_binary)} and executable - {os.access(chrome_binary, os.X_OK)}")
    print(
        f"Chromedriver binary - {chromedriver_path} exists - {os.path.isfile(chromedriver_path)} and executable - {os.access(chromedriver_path, os.X_OK)}")

    main()
