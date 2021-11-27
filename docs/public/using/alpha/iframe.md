
---
title: Selector for element inside iframe
type: using
---



If an element you are trying to use is inside an iframe,
use "in iframe" in the list of elements to refer to an selector
name that uniquely identifies the iframe.



HTML:



iframe.html:

```html
<p id="id_dashboard_message">hello!</a>

```


index.html:

```html
<div id="id_login_page" class="form-login">
<input type="text" id="id_username" class="form-control input-sm chat-input" placeholder="username" /></br>
<input type="text" id="id_password" class="form-control input-sm chat-input" placeholder="password" /></br>
<div class="wrapper">
<span class="group-btn">
<a id="id_ok_button" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
</span>
</div>
</div>

```


dashboard.html:

```html
<div class="form-login">
  <h4 id="id_this_is_a_dashboard_element">Dashboard</h4>
  <iframe id="message_iframe" src="iframe.html" />
</div>

```





selectors.yml:

```yaml
login:
  appears when: login page
  elements:
    login page: id=id_login_page
    username:
      id: id_username
    password:
      id: id_password
    ok:
      id: id_ok_button
dashboard:
  appears when: dashboard identifier
  elements:
    dashboard identifier: id=id_this_is_a_dashboard_element
    message iframe: id=message_iframe
    message:
      in iframe: message iframe
      id: id_dashboard_message

```

set up:

```yaml
from seleniumdirector import WebDirector
from selenium import webdriver

driver = webdriver.Chrome()
selector = WebDirector(driver, "../selectors.yml", default_timeout=5)

```




Successful:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("username").send_keys("login")
selector.the("password").send_keys("password")
selector.the("ok").click()
selector.wait_for_page("dashboard")
selector.the("message").should_be_on_page()
selector.the("message").should_contain("hello!")
driver.quit()

```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/iframe.story">iframe.story</a>.
{{< /note >}}
