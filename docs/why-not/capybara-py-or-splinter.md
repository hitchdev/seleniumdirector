---
title: Why not use Capybara-Py or Splinter?
---

Capybara-Py (and Capybara) and Splinter are both wrappers around selenium
which can be used to write acceptance tests.

Similar to seleniumdirector, both wrap around a selenium Webdriver object
and provide a nicer API on it. They by and large provide all the same
functionality that selenium does.

Seleniumdirector is different because separates selector management
from actions on elements. Selectors are specified in a YAML file while
actions are executed with code. This separation of concerns helps
keep the code and the selector management simpler.

This allows:

* Code that actually interacts with the page elements to be easier to read and simpler to maintain as it just interacts with labels.
* Selector management to be done by a non-programmer.
* Seamless integration with [hitchstory](/hitchstory) and the ability to flexibly write complex stories with the absolute minimum of code.

Capybara-py example [from the docs](https://elliterate.github.io/capybara.py/):

```python
find("xpath", "//table/tr").click()
```

Equivalent seleniumdirector code:

```python
director.the("first table row").click()
```

And YAML:


```yaml
my page:
  first table row:
    xpath: //table/tr
```
