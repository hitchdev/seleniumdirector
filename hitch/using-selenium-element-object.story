Using a selenium element object:
  based on: Selector for element inside iframe
  docs: using-selenium-element-object
  about: |
    If you want to use a selenium object directly (e.g. to implement functionality which
    seleniumdirector doesn't have), you can use .element.

    It's generally a good idea to use the element's iframe context manager. If your element
    isn't in an iframe it does nothing. If there is an iframe it switches to it.
  variations:
    Successful:
      steps:
      - Run: |
          selector.visit("http://localhost:8000")
          selector.wait_for_page("login")

          # Not strictly necessary
          with selector.the("username").iframe:
              selector.the("username").element.send_keys("login")

          # Not strictly necessary
          with selector.the("password").iframe:
              selector.the("password").send_keys("password")

          selector.the("ok").click()
          selector.wait_for_page("dashboard")

          # Necessary
          with selector.the("message").iframe:
              selector.the("message").element.click()

          selector.the("message").should_contain("hello!")

          driver.quit()
