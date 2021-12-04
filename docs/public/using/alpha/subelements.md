
---
title: Sub-elements
---



This example demonstrates both how to reference subelements (using subelements:)
as well as how to select elements by selector and asking for the parent (using but parent:).

It also shows how to grab these subelements - i.e. parent name / child name.

This is an useful feature when grabbing things in groups or tables.



HTML:



index.html:

```html
<div id="dashboard">
  <h4>Dashboard</h4>
  <table id="founder_table">
    <thead>
      <th>Name</th>
      <th>Age</th>
      <th>Company</th>
    </thead>
    <tbody>
    <tr>
      <td class="col_name">Bill Gates</td>
      <td class="col_age">35</td>
      <td class="col_company">Microsoft</td>
    </tr>
    <tr>
      <td class="col_name">Paul Allen</td>
      <td class="col_age">33</td>
      <td class="col_company">Microsoft</td>
    <tr>
    </tr>
      <td class="col_name">Steve Jobs</td>
      <td class="col_age">29</td>
      <td class="col_company">Apple</td>
    </tr>
    </tbody>
  </table>
</div>

```





selectors.yml:

```yaml
dashboard:
  appears when: dashboard
  elements:
    dashboard: id=dashboard
    founder table:
      id: founder_table

      subelements:
        bill gates:
          text is: Bill Gates
          but parent: 1

          subelements:
            age:
              class: col_age

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
selector.wait_for_page("dashboard")
selector.the("founder table / bill gates / age").should_contain("35")

```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/seleniumdirector/blob/master/hitch/story/sub-elements.story">sub-elements.story</a>..

