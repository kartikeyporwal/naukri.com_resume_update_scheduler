import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

gChromeOptions = webdriver.ChromeOptions()
gChromeOptions.add_argument("window-size=1920x1480")
gChromeOptions.add_argument("disable-dev-shm-usage")
gDriver = webdriver.Chrome(
    chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
)
gDriver.get("https://www.python.org/")
time.sleep(3)
gDriver.save_screenshot("my_screenshot.png")
gDriver.close()
