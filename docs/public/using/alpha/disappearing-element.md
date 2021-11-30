
---
title: Element should not be on page
---



The following example shows a 'loading overlay' element which must disappear
before the page can be interacted with.

Using .should_not_be_on_page(after=seconds) selenium director can wait
for the absence of the element and, if it is still there after a timeout,
raise an exception.

This is also useful for writing stories to invoke bugs that accidentally
display elements that shouldn't be there.



HTML:



index.html:

```html
<div class="form-login">
  <h4>Dashboard</h4>
  <p id="id_dashboard_message">hello!</a>
</div>

```




Javascript embedded in above HTML:

```javascript

```


selectors.yml:

```yaml
dashboard:
  appears when: overlay
  elements:
    overlay: id=overlay
    dashboard message: id=id_dashboard_message
    nonexistent element: id=nonexistent_element

```

set up:

```yaml
from seleniumdirector import WebDirector
from selenium import webdriver

driver = webdriver.Chrome()
selector = WebDirector(driver, "../selectors.yml", default_timeout=5)

```




successful disappearance or never on page:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("dashboard")
selector.the("overlay").should_not_be_on_page(after=2)
selector.the("nonexistent element").should_not_be_on_page(after=2)
selector.the("dashboard message").click()

```






if still on page after timeout raise exception:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("dashboard")
selector.the("overlay").should_not_be_on_page(after=0.5)

```


Raises:

```python
seleniumdirector.exceptions.ElementStillOnPage:
overlay still on page after 0.5 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/element-should-not-be-present.story">element-should-not-be-present.story</a>..

