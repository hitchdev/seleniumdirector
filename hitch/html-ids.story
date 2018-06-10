Selectors with HTML IDs:
  based on: login page
  given:
    selectors.yml: |
      login:
        appears when: id=id_this_is_a_login_page
        elements:
          username: id=id_username
          password: id=id_password
          ok: id=id_ok_button
      dashboard:
        appears when: id=id_this_is_a_dashboard_element
        elements:
          message: id=id_dashboard_message
  
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
        <div id="id_this_is_a_dashboard_element" class="form-login">
          <h4>Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
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
          selector.the("message").should_appear()
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
            <div id="id_this_is_a_dashboard_element" class="form-login">
              <h4>Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
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
            selector.the("message").should_appear()
          raises:
            type: seleniumdirector.exceptions.MoreThanOneElement
            message: |-
              More than one element matches your query '//*[@id='id_dashboard_message']'.
