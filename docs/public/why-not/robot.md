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

This combines selectors with the natural flow of the user story, making what should be
an easy to read story a confusing mix of code and story.

SeleniumDirector combined with HitchStory naturally separates these concerns.

Selectors are kept in a separate file from the story, so that the story is more readable
and the selectors can be edited independently.
