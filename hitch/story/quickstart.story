Selectors with HTML IDs:
  docs: html-ids
  about: |
    This example demonstrates how to look for of HTML IDs to
    select and use HTML elements by using 'id=class_name' or 'id: class_name'.

    This is often the ideal kind of selector to use if an element has an ID, since IDs tend to be
    relatively unchanging and the likelihood of accidentally selecting the wrong element is low.

    If there is more than one element matching a ID (shouldn't be common since that's a 
    violation of HTML semantics, but it still happens!), the element to use can be
    specified using 'which: [ number ]' or which: last.
  based on: default
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier: id=id_username
          username: id=id_username
          password: id=id_password
          ok: id=id_ok_button
      dashboard:
        appears when: dashboard identifier
        elements:
          dashboard identifier:
            id: id_this_is_a_dashboard_element
          message:
            id: id_dashboard_message

    website:
      index.html: |
        <div class="form-login">
        <input type="text" id="id_username" class="form-control input-sm chat-input" placeholder="username" /></br>
        <input type="text" id="id_password" class="form-control input-sm chat-input" placeholder="password" /></br>
        <div class="wrapper">
        <span class="group-btn">     
        <a id="id_ok_button" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
        </span>
        </div>
        </div>
      dashboard.html: |
        <div class="form-login">
          <h4 id="id_this_is_a_dashboard_element">Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
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

    More than one ID:
      given:
        website:
          index.html: |
            <div id="id_this_is_a_login_page" class="form-login">
            <input type="text" id="id_username" class="form-control input-sm chat-input" placeholder="username" /></br>
            <input type="text" id="id_password" class="form-control input-sm chat-input" placeholder="password" /></br>
            <div class="wrapper">
            <span class="group-btn">     
            <a id="id_ok_button" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
            </span>
            </div>
            </div>
          dashboard.html: |
            <div class="form-login">
              <h4 id="id_this_is_a_dashboard_element">Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
              <h4>Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
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
              More than one element matches your query '//*[@id='id_dashboard_message']'.
