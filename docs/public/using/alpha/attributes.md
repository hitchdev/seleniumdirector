
---
title: With HTML attributes
---



This example demonstrates how to use HTML attributes to select and use
HTML elements by using 'attribute: attrib-name=attrib-value'.

If there is more than one element matching that attribute, the element
to use can be specified using 'which: [ number ]' or which: last.



HTML:



index.html:

```html
<div data-id="login-page" class="form-login">
<input type="text" data-id="username" class="form-control input-sm chat-input" placeholder="username" /></br>
<input type="text" data-id="password" class="form-control input-sm chat-input" placeholder="password" /></br>
<div class="wrapper">
<span class="group-btn">
<a data-id="ok" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
</span>
</div>
</div>

```


dashboard.html:

```html
<div data-id="this-is-a-dashboard-element" class="form-login">
  <h4>Dashboard</h4>  <p data-id="this-is-a-message">hello!</a>
  <h4>Dashboard</h4>  <p data-id="this-is-a-message">goodbye!</a>
</div>

```





selectors.yml:

```yaml
login:
  appears when: login page identifier
  elements:
    login page identifier:
      attribute: data-id=login-page
    username:
      attribute: data-id=username
      which: 1
    password:
      attribute: data-id=password
    ok:
      attribute: data-id=ok
dashboard:
  appears when: dashboard identifier
  elements:
    dashboard identifier:
      attribute: data-id=this-is-a-dashboard-element
    message:
      attribute: data-id=this-is-a-message
      which: last

```

set up:

```yaml
from seleniumdirector import WebDirector
from selenium import webdriver

driver = webdriver.Chrome()
selector = WebDirector(driver, "../selectors.yml", default_timeout=5)

```






```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("username").send_keys("login")
selector.the("password").send_keys("password")
selector.the("ok").click()
selector.wait_for_page("dashboard")
selector.the("message").should_be_on_page()
selector.the("message").should_contain("goodbye!")
driver.quit()

```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/seleniumdirector/blob/master/hitch/story/attributes.story">attributes.story</a>..

