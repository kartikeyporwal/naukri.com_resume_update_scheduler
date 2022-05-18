# Naukri.com Resume Update scheduler

A python script that uses selenium webdriver to download latest resume from specified pdf url and update resume on naukri.com every specified seconds  

## Features
- Updates the naukri.com resume every specified seconds
- Fetches latest resume from google docs or any specified pdf url
- Uses chrome driver or geckodriver for automation
- Easily deployable on heroku

## Enviroment Variables

`RUN_EVERY_SECS` - INT -  to update resume after specified seconds  
`RESUME_PDF_URL` - STR - url of the pdf file of resume; use [this](https://support.google.com/a/users/answer/9308985?hl=en) to get pdf url of resume from google docs  
`RESUME_FILE_NAME` - STR - name of the resume, e.g., `kartikey_porwal_resume.pdf` to be uploaded on naukri  

`CHROME_BINARY_PATH` - STR - path of the Google Chrome binary - DEFAULT PATH: `/app/.apt/usr/bin/google-chrome`
`CHROME_WEBDRIVER_PATH` - STR - path of the Chrome Webdriver - DEFAULT PATH: `/app/.chromedriver/bin/chromedriver`

`FIREFOX_BINARY_PATH` - STR - path of the Firefox binary - DEFAULT PATH: `/app/vendor/firefox/firefox`
`GECKO_WEBDRIVER_PATH` - STR - path of the Gecko Webdriver - DEFAULT PATH: `/app/vendor/geckodriver`

`NAUKRI_USER_EMAIL` - STR - naukri.com registered email address  
`NAUKRI_USER_PASSWORD` - STR - naukri.com account password  

`WEBDRIVER_MODE` - STR - CHROME or GECKO; webdriver mode to open particular webdriver  

## Local Test

To run and test the automation locally follow the below mentioned steps

```bash

# Create a new virtual environment
python -m venv test_env

# Activate the virtual environment
source test_env/bin/activate

# Install the necessary packages
python -m pip install -r requirements.txt

# Copy the .env.example file to .env

# Update the environment variables in the .env file

# Run the script
python naukri_resume_update.py


```


```bash

# To know the binary location of Google Chrome browser and set the path to `CHROME_BINARY_PATH`
# default location on ubuntu is /usr/bin/google-chrome-stable
whereis google-chrome-stable
# OR
which google-chrome-stable

# Download the same version of chrome webdriver from https://chromedriver.chromium.org/downloads
# check the current chrome version using `/usr/bin/google-chrome-stable --version`
# and set the path to `CHROME_WEBDRIVER_PATH`


# To know the binary location of Firefox browser and set the path to `FIREFOX_BINARY_PATH`
# default location on ubuntu is /usr/bin/firefox
whereis firefox
# OR
which firefox


# Download the same version of gecko webdriver from https://github.com/mozilla/geckodriver/releases
# check the current chrome version using `/usr/bin/firefox --version`
# and set the path to `GECKO_WEBDRIVER_PATH`


```

## Heroku Configuration

### Buildpacks

For Python - `heroku/python`  
For Google Chrome - `https://github.com/heroku/heroku-buildpack-google-chrome`  
For Google Chromedriver - `https://github.com/heroku/heroku-buildpack-chromedriver`  
For Firefox - `https://github.com/buitron/firefox-buildpack`  
For Geckodriver - `http://github.com/buitron/geckodriver-buildpack`  


### Steps to deploy on Heroku

- Login to `https://dashboard.heroku.com/apps`  
- Click `New` and `create new app`  
- Once app is created, go to setting add above mentioned build packs  
- In `Config Vars` section, click `Reveal Config Vars` and add above mentioned environment variables with their respective values  
- Follow guide on deploy section.


## TO-DOs
- Add Validations to check if logged in successfully  
- Add options to choose different selectors when an element could not located  
- Add config file to specify/change different element when any change occurs on web elements  