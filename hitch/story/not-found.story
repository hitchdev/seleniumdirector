Ok button not found:
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
    not in selectors.yml:
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


    timeout to appear on implicit wait:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("nonexistent").click()
          raises:
            type: seleniumdirector.exceptions.ElementDidNotAppear
            message: |-
              Could not find 'nonexistent' on page 'login' using xpath '//*[@id='not_there']' after default timeout of 5 seconds.

    timeout to appear on explicit wait:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("nonexistent").should_be_on_page()
          raises:
            type: seleniumdirector.exceptions.ElementDidNotAppear
            message: |-
              Could not find 'nonexistent' on page 'login' using xpath '//*[@id='not_there']' after timeout of 5 seconds.

    timeout on element containing text:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("login")
            selector.the("login button").should_contain("logout")
          raises:
            type: seleniumdirector.exceptions.ElementDidNotContain
            message: |-
              Element 'login button' on page 'login' using xpath '//*[@id='id_ok_button']' contained:

              login

              not:

              logout

              after timeout of 5 seconds.
