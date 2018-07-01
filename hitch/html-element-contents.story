Selectors using HTML contents:
  description: |
    This story demonstrates using the textual content of
    HTML elements to select them.
  based on: login page
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier: class=class_username
          username: class=class_username
          password: class=class_password
          login:
            text is: login
      dashboard:
        appears when: dashboard identifier
        elements:
          dashboard identifier:
            class: class_this_is_a_dashboard_element
            which: 1
          first message:
            text contains: hello
            which: 1
          last message:
            text contains: hello
            which: last

    website:
      index.html: |
        <div class="form-login">
        <input type="text" class="class_username form-control input-sm chat-input" placeholder="username" /></br>
        <input type="text" class="class_password form-control input-sm chat-input" placeholder="password" /></br>
        <div class="wrapper">
        <span class="group-btn">
        <a href="#" class="btn btn-primary btn-md">not login <i class="fa fa-sign-in"></i></a>
        <a href="/dashboard.html" class="btn btn-primary btn-md">login<i class="fa fa-sign-in"></i></a>
        </span>
        </div>
        </div>
      dashboard.html: |
        <div class="form-login">
          <h4>Dashboard</h4>
          <p class="class_this_is_a_dashboard_element">hello tom!</p>
          <p class="class_this_is_a_dashboard_element">hello harry!</p>
        </div>

  variations:
    Successful:
      steps:
      - Run: |
          selector.visit("http://localhost:8000")
          selector.wait_for_page("login")
          selector.the("username").send_keys("login")
          selector.the("password").send_keys("password")
          selector.the("login").click()
          selector.wait_for_page("dashboard")
          selector.the("first message").should_be_on_page()
          selector.the("first message").should_contain("hello tom!")
          selector.the("last message").should_contain("hello harry!")
          driver.quit()
