Fake time:
  description: |
    This story demonstrates loading a website that uses javascript
    to get the time and display it on the page.
  given:
    python version: 3.5.0
    selenium version: 3.11.0
    javascript: |
      var now = new Date();

      document.getElementById("id_dashboard_message").innerHTML = now;
    selectors.yml: |
      dashboard:
        appears when: message
        elements:
          message: id=id_dashboard_message

    website:
      index.html: |
        <div class="form-login">
          <h4>Dashboard</h4>
          <p id="id_dashboard_message">hello!</a>
        </div>
    setup: |
      from seleniumdirector import WebSelector
      from selenium import webdriver
      from datetime import datetime

      driver = webdriver.Chrome()

      selector = WebSelector(
          driver,
          "selectors.yml",
          fake_time=datetime(2015, 10, 21, 14, 0, 0),
      )
  steps:
  - Run: |
      selector.visit("http://localhost:8000")
      selector.wait_for_page("dashboard")
      selector.the("message").should_contain("Wed Oct 21 2015 14:00:00")
