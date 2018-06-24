Login page:
  description: |
    This story demonstrates:
    
    - Loading a website.
    - Entering the context of a login page.
    - Using the login page
    - Entering the context of a dashboard page.
    - Using the dashboard page.
    
    selectors.yml is a configuration file that translates
    readable names that are relevant in a page context to
    HTML IDs that are meaningful to selenium.
  given:
    python version: 3.5.0
    selenium version: 3.11.0
    setup: |
      from seleniumdirector import WebDirector
      from selenium import webdriver

      driver = webdriver.Chrome()
      selector = WebDirector(driver, "selectors.yml")
