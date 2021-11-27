---
title: Why not use Robot SeleniumLibrary?
---

Robot's SeleniumLibrary is a layer around selenium designed to integrate it
with the Robot framework. It is designed to create test cases like this:

```
*** Settings ***
Library  SeleniumLibrary

*** Test Cases ***
The user can search for flights
    [Tags]	    search_flights
    Open browser    http://blazedemo.com/   Chrome
    Select From List By Value   xpath://select[@name='fromPort']  Paris
    Select From List by Value   xpath://select[@name='toPort']    London
    Click Button    css:input[type='submit']
    @{flights}=  Get WebElements    css:table[class='table']>tbody tr
    Should Not Be Empty     ${flights}
    Close All Browsers

```

Example taken from https://www.blazemeter.com/blog/robot-framework-the-ultimate-guide-to-running-your-tests

[ TODO : Two concerns smushed together ]
