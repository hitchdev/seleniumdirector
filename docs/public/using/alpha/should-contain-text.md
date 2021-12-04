
---
title: Should contain text
---



This example demonstrates .should_contain("text") which first waits
for the specified element to appear and then waits for it to contain
part or all of the text specified.



HTML:



index.html:

```html
<div class="form-login">
<input type="text" id="id_username" class="form-control input-sm chat-input" placeholder="username" /></br>
<input type="text" id="id_password" class="form-control input-sm chat-input" placeholder="password" /></br>
<div class="wrapper">
<span class="group-btn">
<a id="id_ok_button" href="/dashboard.html" class="btn btn-primary btn-md">login <i class="fa fa-sign-in"></i></a>
</span>
</div>
</div>

```





selectors.yml:

```yaml
login:
  appears when: login page identifier
  elements:
    login page identifier: id=id_username
    login button: id=id_ok_button
    nonexistent: id=not_there

```

set up:

```yaml
from seleniumdirector import WebDirector
from selenium import webdriver

driver = webdriver.Chrome()
selector = WebDirector(driver, "../selectors.yml", default_timeout=5)

```




successful:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("login button").should_contain("log", after=5)

```






timeout on element containing text:




```python
selector.visit("http://localhost:8000")
selector.wait_for_page("login")
selector.the("login button").should_contain("logout", after=5)

```


Raises:

```python
seleniumdirector.exceptions.ElementDidNotContain:
Element 'login button' on page 'login' using xpath '//*[@id='id_ok_button']' contained:

login

not:

logout

after timeout of 5 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/seleniumdirector/blob/master/hitch/story/should-contain-text.story">should-contain-text.story</a>..

