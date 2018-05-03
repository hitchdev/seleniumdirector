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
      from seleniumdirector import WebSelector
      from selenium import webdriver

      driver = webdriver.Chrome()
      selector = WebSelector(driver, "selectors.yml")
  steps:
  - Run: |
      selector.visit("http://localhost:8000")
      selector.wait_for_page("login")
      selector.the("username").send_keys("login")
      selector.the("password").send_keys("password")
      selector.the("ok").click()
      selector.wait_for_page("dashboard")
      selector.the("message").should_contain("hello!")
      driver.quit()
