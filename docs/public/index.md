---
title: SeleniumDirector
---


<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/seleniumdirector?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/seleniumdirector">





SeleniumDirector is a python 3 library that makes it straightforward to write easily maintainable 
python code to interact with websites in a non-brittle way using the screenplay pattern with
selenium.

Seleniumdirector reads YAML "selector" files which associate readable labels with complex selectors
- i.e. class name selectors, id selectors, attribute selectors, text and xpath.

Separating the "element selection" concern from element interaction allows for simpler, more straightforward
and more readable code.

SeleniumDirector was built to be used with [HitchStory](https://hitchdev.com/hitchstory) as a means
of writing straightforward to maintain integration/browser tests, but it completely agnostic about
where it is used. It can be used in py.test, nose or unittest or it could be used to direct other forms
of automated website interaction - e.g. as a scraper.



## Example




This example demonstrates how to look for of HTML IDs to
select and use HTML elements by using 'id=class_name' or 'id: class_name'.

This is often the ideal kind of selector to use if an element has an ID, since IDs tend to be
relatively unchanging and the likelihood of accidentally selecting the wrong element is low.

If there is more than one element matching a ID (shouldn't be common since that's a 
violation of HTML semantics, but it still happens!), the element to use can be
specified using 'which: [ number ]' or which: last.



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


dashboard.html:

```html
<div class="form-login">
  <h4 id="id_this_is_a_dashboard_element">Dashboard</h4>  <p id="id_dashboard_message">hello!</a>
</div>

```





selectors.yml:

```yaml
login:
  appears when: login page identifier
  elements:
    login page identifier: id=id_username
    username: id=id_username
    password: id=id_password
    ok: id=id_ok_button
dashboard:
  appears when: dashboard identifier
  elements:
    dashboard identifier:
      id: id_this_is_a_dashboard_element
    message:
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






More than one ID:




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
More than one element matches your query '//*[@id='id_dashboard_message']'.
```













## Install with pip

```bash
$ pip install seleniumdirector
```

You can also use hitchkey to generate a skeleton project structure along
with [hitchstory](https://hitchdev.com/hitchstory/).

Either install hitchkey with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipsi install hitchkey
```

Or, if you'd prefer, you can safely install with "sudo pip" (deactivate any virtualenvs you're in):

```bash
sudo pip install hitchkey
```

Once hitchkey is installed:

```bash
cd /your/project/directory
hk --demo seleniumdirector
```

This will create a directory called "hitch" and put three files in it, including one story, which you can play by running:

```bash
hk bdd logged in
```


## Using SeleniumDirector

- [Selector for element inside iframe](using/alpha/)
- [Sub-elements](using/alpha/)
- [Selectors with HTML classes](using/alpha/)
- [With HTML attributes](using/alpha/)
- [Overlay - should_be_on_top](using/alpha/)
- [Element should not be on page](using/alpha/)
- [Selectors using HTML contents](using/alpha/)
- [Using a selenium element object](using/alpha/)
- [Hover - hovering over an element](using/alpha/)
- [Should contain text](using/alpha/)
- [Selectors with HTML IDs](using/alpha/)



## Why not X instead?

- [Why not use Robot SeleniumLibrary?](why-not/)
- [Why not use the page object pattern?](why-not/)
- [Why not use Capybara-Py or Splinter?](why-not/)



## Contributors:

- Chaitu Shantharam