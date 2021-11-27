
---
title: Selectors with HTML classes
type: using
---



This example demonstrates how to look for the presence of HTML classes to
select and use HTML elements by using 'class=class_name' or 'class: class_name'.

If there is more than one element matching a class (common, since that's how classes
are supposed to be used), the element to use can be specified using 'which: [ number ]'
or which: last.



HTML:



index.html:

```html
<div class="class_this_is_a_login_page form-login">
<input type="text" class="class_username form-control input-sm chat-input" placeholder="username" /></br>
<input type="text" class="class_password form-control input-sm chat-input" placeholder="password" /></br>
<div class="wrapper">
<span class="group-btn">
<a href="/dashboard.html" class="class_ok btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
</span>
</div>
</div>

```


dashboard.html:

```html
<div class="class_this_is_a_dashboard_element form-login">
  <h4>Dashboard</h4>  <p class="class_dashboard_element">hello!</a>
</div>

```





selectors.yml:

```yaml
login:
  appears when: login page identifier
  elements:
    login page identifier: class=class_this_is_a_login_page
    username: class=class_username
    password: class=class_password
    ok: class=class_ok
dashboard:
  appears when: dashboard identifier
  elements:
    dashboard identifier:
      class: class_this_is_a_dashboard_element
    message:
      class: class_dashboard_element

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






More than one element with a class causes error:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("username").send_keys("login")
selector.the("password").send_keys("password")
selector.the("ok").click()
selector.wait_for_page("dashboard")
selector.the("message").should_be_on_page()

```


Raises:

```python
seleniumdirector.exceptions.MoreThanOneElement:
More than one element matches your query '//*[contains(concat(' ', normalize-space(@class), ' '), ' class_dashboard_element ')]'.
```






More than one element with a class - select the first and last:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("username").send_keys("login")
selector.the("password").send_keys("password")
selector.the("ok").click()
selector.wait_for_page("dashboard")
selector.the("first message").should_be_on_page()
selector.the("first message").should_contain("hello!")
selector.the("last message").should_contain("goodbye!")
driver.quit()

```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/html-classes.story">html-classes.story</a>.
{{< /note >}}
