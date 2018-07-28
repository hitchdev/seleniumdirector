Should contain text:
  based on: default
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier: id=id_username
          login button: id=id_ok_button
          nonexistent: id=not_there
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
    timeout on element containing text:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("login button").should_contain("logout", after=5)
          raises:
            type: seleniumdirector.exceptions.ElementDidNotContain
            message: |-
              Element 'login button' on page 'login' using xpath '//*[@id='id_ok_button']' contained:

              login

              not:

              logout

              after timeout of 5 seconds.
