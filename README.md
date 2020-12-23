# Naukri.com Resume Update scheduler

## Features
- Updates the naukri.com resume every specified seconds
- Fetches latest resume from google docs
- Uses geckodriver for automation
- Easy deployable on heroku

## Enviroment Variables

`RUN_EVERY_SECS` - INT -  to update resume after specified seconds  
`RESUME_PDF_URL` - STR - url of the pdf file of resume; use [this](https://support.google.com/a/users/answer/9308985?hl=en) to get pdf url of resume from google docs  

`GOOGLE_CHROME_BIN` - STR - path of the Google Chrome binary  
`CHROME_WEBDRIVER_PATH` - STR - path of the Chrome Webdriver  

`FIREFOX_BINARY_PATH` - STR - path of the Firefox binary  
`GECKO_WEBDRIVER_PATH` - STR - path of the Gecko Webdriver  

`NAUKRI_USER_EMAIL` - STR - naukri.com registered email address  
`NAUKRI_USER_PASSWORD` - STR - naukri.com account password  

`WEBDRIVER_MODE` - STR - CHROME or GECKO; webdriver mode to open particular webdriver


## Sample log

remote: -----> Extracting Firefox binaries to /tmp/build_2b383b7a/vendor/firefox
remote: -----> geckodriver app detected
remote: -----> Searching for latest geckodriver version...
remote: -----> Found geckodriver version: v0.28.0
remote: -----> Extracting geckodriver binaries to /tmp/build_2b383b7a/vendor/geckodriver