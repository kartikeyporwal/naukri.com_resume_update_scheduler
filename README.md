# Naukri.com Resume Update scheduler
A python script uses selenium webdriver to download latest resume from specified pdf url and update resume on naukri.com every specified seconds  

## Features
- Updates the naukri.com resume every specified seconds
- Fetches latest resume from google docs or any specified pdf url
- Uses chrome driver or geckodriver for automation
- Easy deployable on heroku

## Enviroment Variables

`RUN_EVERY_SECS` - INT -  to update resume after specified seconds  
`RESUME_PDF_URL` - STR - url of the pdf file of resume; use [this](https://support.google.com/a/users/answer/9308985?hl=en) to get pdf url of resume from google docs  

`GOOGLE_CHROME_BIN` - STR - path of the Google Chrome binary - DEFAULT PATH: `/app/.apt/usr/bin/google-chrome`
`CHROME_WEBDRIVER_PATH` - STR - path of the Chrome Webdriver - DEFAULT PATH: `/app/.chromedriver/bin/chromedriver`

`FIREFOX_BINARY_PATH` - STR - path of the Firefox binary - DEFAULT PATH: `/app/vendor/firefox/firefox`
`GECKO_WEBDRIVER_PATH` - STR - path of the Gecko Webdriver - DEFAULT PATH: `/app/vendor/geckodriver`

`NAUKRI_USER_EMAIL` - STR - naukri.com registered email address  
`NAUKRI_USER_PASSWORD` - STR - naukri.com account password  

`WEBDRIVER_MODE` - STR - CHROME or GECKO; webdriver mode to open particular webdriver  

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