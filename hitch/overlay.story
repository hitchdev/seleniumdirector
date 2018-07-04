Overlay - should_be_on_top:
  based on: default
  description: |
    This story demonstrates .should_be_on_top() which waits not
    only for an element to be present on the page (without display:none set),
    it will wait until no other element covers it.
  given:
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

      director = seleniumdirector.WebDirector(
          driver,
          "selectors.yml",
          fake_time=datetime(2015, 10, 21, 7, 28, 0),
      )
  variations:
    Success:
      given:
        javascript: |
          $(document).ready(function() {
            displayOverlay("Loading...")
            setTimeout(function(){ removeOverlay(); }, 1000);
          })
      steps:
      - Run: |
          director.visit("http://localhost:8000")
          director.wait_for_page("dashboard")
          director.the("message").should_be_on_top()
          director.the("message").click()

    Failure:
      given:
        javascript: |
          $(document).ready(function() {
            displayOverlay("Loading...")
            setTimeout(function(){ removeOverlay(); }, 1000);
          })
      steps:
      - Run:
          code: |
            director.visit("http://localhost:8000")
            director.wait_for_page("dashboard")
            director.the("message").should_be_on_top(after=0.5)
            director.the("message").click()
          raises:
            type: seleniumdirector.exceptions.ElementCoveredByAnotherElement
            message: |-
              Another element, a 'td' with id '' and class '' is covering yours '//*[@id='id_dashboard_message']'.
