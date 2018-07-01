Ok button not found:
  based on: login page
  given:
    selectors.yml: |
      login:
        appears when: login page identifier
        elements:
          login page identifier: id=id_username
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


    timeout implicit:
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

    timeout explicit:
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
