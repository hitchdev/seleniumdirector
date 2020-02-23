Element should not be on page:
  docs: disappearing-element
  about: |
    The following example shows a 'loading overlay' element which must disappear
    before the page can be interacted with.
    
    Using .should_not_be_on_page(after=seconds) selenium director can wait
    for the absence of the element and, if it is still there after a timeout,
    raise an exception.
    
    This is also useful for writing stories to invoke bugs that accidentally
    display elements that shouldn't be there.
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

    if still on page after timeout raise exception:
      steps:
      - Run:
          code: |
            selector.visit("http://localhost:8000")
            selector.wait_for_page("dashboard")
            selector.the("overlay").should_not_be_on_page(after=0.5)
          raises:
            type: seleniumdirector.exceptions.ElementStillOnPage
            message: overlay still on page after 0.5 seconds.
