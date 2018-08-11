Element should not be on page:
  based on: default
  given:
    selectors.yml: |
      dashboard:
        appears when: overlay
        elements:
          overlay: id=overlay
          dashboard message: id=id_dashboard_message
          nonexistent element: id=nonexistent_element

    javascript: |
      $(document).ready(function() {
        displayOverlay("Loading...")
        setTimeout(function(){ removeOverlay(); }, 1000);
      })

    website:
      index.html: |
        <div class="form-login">
          <h4>Dashboard</h4>
          <p id="id_dashboard_message">hello!</a>
        </div>

  variations:
    successful disappearance or never on page:
      steps:
      - Run: |
          selector.visit("http://localhost:8000")
          selector.wait_for_page("dashboard")
          selector.the("overlay").should_not_be_on_page(after=2)
          selector.the("nonexistent element").should_not_be_on_page(after=2)
          selector.the("dashboard message").click()

    still on page:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("dashboard")
            selector.the("overlay").should_not_be_on_page(after=0.5)
            selector.the("dashboard message").click()
          raises:
            type: seleniumdirector.exceptions.ElementStillOnPage
            message: overlay still on page after 0.5 seconds.
