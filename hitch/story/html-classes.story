Selectors with HTML classes:
  docs: html-classes
  about: |
    This example demonstrates how to look for the presence of HTML classes to
    select and use HTML elements by using 'class=class_name' or 'class: class_name'.

    If there is more than one element matching a class (common, since that's how classes
    are supposed to be used), the element to use can be specified using 'which: [ number ]'
    or which: last.
  based on: default
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier: class=class_this_is_a_login_page
          username: class=class_username
          password: class=class_password
          ok: class=class_ok
      dashboard:
        appears when: dashboard identifier
        elements:
          dashboard identifier:
            class: class_this_is_a_dashboard_element
          message:
            class: class_dashboard_element

    website:
      index.html: |
        <div class="class_this_is_a_login_page form-login">
        <input type="text" class="class_username form-control input-sm chat-input" placeholder="username" /></br>
        <input type="text" class="class_password form-control input-sm chat-input" placeholder="password" /></br>
        <div class="wrapper">
        <span class="group-btn">
        <a href="/dashboard.html" class="class_ok btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
        </span>
        </div>
        </div>
      dashboard.html: |
        <div class="class_this_is_a_dashboard_element form-login">
          <h4>Dashboard</h4>  <p class="class_dashboard_element">hello!</a>
        </div>

  variations:
    Successful:
      steps:
      - Run: |
          selector.visit("http://localhost:8000")
          selector.wait_for_page("login")
          selector.the("username").send_keys("login")
          selector.the("password").send_keys("password")
          selector.the("ok").click()
          selector.wait_for_page("dashboard")
          selector.the("message").should_be_on_page()
          selector.the("message").should_contain("hello!")
          driver.quit()

    More than one element with a class causes error:
      given:
        website:
          index.html: |
            <div class="class_this_is_a_login_page form-login">
            <input type="text" class="class_username form-control input-sm chat-input" placeholder="username" /></br>
            <input type="text" class="class_password form-control input-sm chat-input" placeholder="password" /></br>
            <div class="wrapper">
            <span class="group-btn">
            <a href="/dashboard.html" class="class_ok btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
            </span>
            </div>
            </div>
          dashboard.html: |
            <div class="class_this_is_a_dashboard_element form-login">
              <h4>Dashboard</h4>  <p class="class_dashboard_element">hello!</a>
              <h4>Dashboard</h4>  <p class="class_dashboard_element">hello!</a>
            </div>
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("username").send_keys("login")
            selector.the("password").send_keys("password")
            selector.the("ok").click()
            selector.wait_for_page("dashboard")
            selector.the("message").should_be_on_page()
          raises:
            type: seleniumdirector.exceptions.MoreThanOneElement
            message: |-
              More than one element matches your query '//*[contains(concat(' ', normalize-space(@class), ' '), ' class_dashboard_element ')]'.


    More than one element with a class - select the first and last:
      given:
        selectors.yml: |
          login:
            appears when: login page identifier
            elements:
              login page identifier: class=class_this_is_a_login_page
              username: class=class_username
              password: class=class_password
              ok: class=class_ok
          dashboard:
            appears when: dashboard identifier
            elements:
              dashboard identifier:
                class: class_this_is_a_dashboard_element
              first message:
                class: class_dashboard_element
                which: 1
              last message:
                class: class_dashboard_element
                which: last
        website:
          index.html: |
            <div class="class_this_is_a_login_page form-login">
            <input type="text" class="class_username form-control input-sm chat-input" placeholder="username" /></br>
            <input type="text" class="class_password form-control input-sm chat-input" placeholder="password" /></br>
            <div class="wrapper">
            <span class="group-btn">
            <a href="/dashboard.html" class="class_ok btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
            </span>
            </div>
            </div>
          dashboard.html: |
            <div class="class_this_is_a_dashboard_element form-login">
              <h4>Dashboard</h4>  <p class="class_dashboard_element">hello!</a>
              <h4>Dashboard</h4>  <p class="class_dashboard_element">goodbye!</a>
            </div>
      steps:
      - Run: |
          selector.visit("http://localhost:8000")
          selector.wait_for_page("login")
          selector.the("username").send_keys("login")
          selector.the("password").send_keys("password")
          selector.the("ok").click()
          selector.wait_for_page("dashboard")
          selector.the("first message").should_be_on_page()
          selector.the("first message").should_contain("hello!")
          selector.the("last message").should_contain("goodbye!")
          driver.quit()
