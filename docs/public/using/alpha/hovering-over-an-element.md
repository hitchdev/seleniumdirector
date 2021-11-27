
---
title: Hover - hovering over an element
type: using
---



This example demonstrates hovering over an element. The method .hover()
will act as if you are hovering over your mouse on an html element

This example will show hovering over an element called 'hover element' and
that will make a message appear saying 'Now You See Me'.



HTML:



index.html:

```html
<div class="form-login">
  <p id="id_main_hovered_element">Hover Over Me</a>
  <p style="display:none;" id="id_revealed_element">Now You See Me</a>
</div>

```




Javascript embedded in above HTML:

```javascript

```


selectors.yml:

```yaml
dashboard:
  appears when: main hovered element
  elements:
    main hovered element: id=id_main_hovered_element
    revealed element: id=id_revealed_element

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
import time
director.the("main hovered element").hover()
director.the("revealed element").should_be_on_page()

```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/hover.story">hover.story</a>.
{{< /note >}}
