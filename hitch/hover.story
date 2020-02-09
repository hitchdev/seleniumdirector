Hover - hovering over an element:
  docs: hovering-over-an-element
  based on: default
  about: |
    This example demonstrates hovering over an element. The method .hover()
    will act as if you are hovering over your mouse on an html element

    This example will show hovering over an element called 'hover element' and
    that will make a message appear saying 'Now You See Me'.
  given:
    javascript: |
      $(document).ready(function() {
        $("#id_main_hovered_element").mouseover(function() {
          $("#id_revealed_element").show()
        })
      })
    selectors.yml: |
      dashboard:
        appears when: main hovered element
        elements:
          main hovered element: id=id_main_hovered_element
          revealed element: id=id_revealed_element

    website:
      index.html: |
        <div class="form-login">
          <p id="id_main_hovered_element">Hover Over Me</a>
          <p style="display:none;" id="id_revealed_element">Now You See Me</a>
        </div>
    setup: |
      from selenium import webdriver
      from datetime import datetime
      import seleniumdirector

      driver = webdriver.Chrome()

      director = seleniumdirector.WebDirector(
          driver,
          "../selectors.yml",
      )
  variations:
    Success:
      steps:
      - Run: |
          director.visit("http://localhost:8000")
          director.wait_for_page("dashboard")
          import time
          director.the("main hovered element").hover()
          director.the("revealed element").should_be_on_page()
