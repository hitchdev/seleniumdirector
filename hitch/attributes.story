With xpath or attributes:
  based on: login page
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier:
            attribute: data-id=login-page
          username:
            xpath: (//*[@data-id='username'])[1]
          password:
            attribute: data-id=password
          ok:
            xpath: (//*[@data-id='ok'])[1]
      dashboard:
        appears when: dashboard identifier
        elements:
          dashboard identifier:
            attribute: data-id=this-is-a-dashboard-element
          message:
            xpath: (//*[@data-id='this-is-a-message'])[1]

    website:
      index.html: |
        <div data-id="login-page" class="form-login">
        <input type="text" data-id="username" class="form-control input-sm chat-input" placeholder="username" /></br>
        <input type="text" data-id="password" class="form-control input-sm chat-input" placeholder="password" /></br>
        <div class="wrapper">
        <span class="group-btn">     
        <a data-id="ok" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
        </span>
        </div>
        </div>
      dashboard.html: |
        <div data-id="this-is-a-dashboard-element" class="form-login">
          <h4>Dashboard</h4>  <p data-id="this-is-a-message">hello!</a>
        </div>
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
