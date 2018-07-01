Ok button not found:
  based on: login page
  given:
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

  variations:
    not in selectors.yml:
      given:
        selectors.yml: |
          login:
            appears when: login page identifier
            elements:
              login page identifier: id=id_username

      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("ok").click()
          raises:
            type: seleniumdirector.exceptions.NotFoundInSelectors
            message: |-
              'ok' not found in selectors file for page 'login'.
