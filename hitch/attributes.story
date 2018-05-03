With xpath or attributes:
  based on: login page
  given:
    selectors.yml: |
      login:
        appears when:
          attribute: data-id=login-page
        elements:
          username:
            xpath: (//*[@data-id='username'])[1]
          password:
            attribute: data-id=password
          ok:
            xpath: (//*[@data-id='ok'])[1]
      dashboard:
        appears when:
          attribute: data-id=this-is-a-dashboard-element
        elements:
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
