Overlay - should_be_on_top:
  description: |
    This story demonstrates .should_be_on_top() which waits not
    only for an element to be present on the page (without display:none set),
    it will wait until no other element covers it.
  given:
    python version: 3.5.0
    selenium version: 3.11.0
    javascript: |
      $(document).ready(function() {
        displayOverlay("Loading...")
        setTimeout(function(){ removeOverlay(); }, 1000);
      })
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
      from selenium import webdriver
      from datetime import datetime
      import seleniumdirector

      driver = webdriver.Chrome()

      selector = seleniumdirector.WebDirector(
          driver,
          "selectors.yml",
          fake_time=datetime(2015, 10, 21, 7, 28, 0),
      )
  steps:
  - Run: |
      selector.visit("http://localhost:8000")
      selector.wait_for_page("dashboard")
      selector.the("message").should_be_on_top()
      selector.the("message").click()
