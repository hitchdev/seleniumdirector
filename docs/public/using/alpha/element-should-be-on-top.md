
---
title: Overlay - should_be_on_top
type: using
---



This example demonstrates .should_be_on_top() which waits not
only for an element to be present on the page (without display:none set),
it will wait until no other element covers it.

should_be_on_top checks the dead center of the element to see
if it is covered. If the middle is covered and the corners are not then
it will still think that the element is covered.



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
  appears when: message
  elements:
    message: id=id_dashboard_message

```

set up:

```yaml
from selenium import webdriver
from datetime import datetime
import seleniumdirector

driver = webdriver.Chrome()

director = seleniumdirector.WebDirector(
    driver,
    "../selectors.yml",
)

```




Success:




```python
director.visit("http://localhost:8000")
director.wait_for_page("dashboard")
director.the("message").should_be_on_top()
director.the("message").click()

```






Failure:




```python
director.visit("http://localhost:8000")
director.wait_for_page("dashboard")
director.the("message").should_be_on_top(after=0.2)
director.the("message").click()

```


Raises:

```python
seleniumdirector.exceptions.ElementCoveredByAnotherElement:
Another element, a 'td' with id '' and class '' is covering yours '//*[@id='id_dashboard_message']'.
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/overlay.story">overlay.story</a>.
{{< /note >}}
