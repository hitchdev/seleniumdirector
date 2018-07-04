Default:
  given:
    python version: 3.5.0
    selenium version: 3.11.0
    setup: |
      from seleniumdirector import WebDirector
      from selenium import webdriver

      driver = webdriver.Chrome()
      selector = WebDirector(driver, "selectors.yml", default_timeout=5)
