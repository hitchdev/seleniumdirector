---
title: Why not use the page object pattern?
---

The [page object pattern](https://www.martinfowler.com/bliki/PageObject.html) is a design pattern for creating a code API abstraction around web pages to simplify their usage in GUI tests. 

The idea of the page object pattern is is to enact a [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) between the code that interacts directly with HTML and the code which interacts with the web application.

While identifying a real problem and proposing a solution that works to solve that problem, it is not the most elegant solution to that problem. There are two major problems with this approach:



1. It separates the wrong concerns
----------------------------------

Every script script that interacts with a web page performs a series of actions on a set of elements. While the the process to locate those elements is often complex, the actions performed on them are, by and large, not - the elements are clicked, they have text entered or one element is dragged on to another.

What is often obvious to the user (e.g. username text box) is often ambiguous to code. This is, in part, because HTML's design did not make this easy. However, HTML is here and we're stuck with it so we need to deal with it and this complexity has to be isolated.

Selenium has a number of different kinds of selectors (ID, class, attribute, xpath) each of which is appropriate to use in multitude of different situations. None of this is remotely interesting to anybody except the person writing the test - users just want to grab elements and perform actions upon them. Whether an element is grabbed by a class selector or an ID selector is of no importance, but precisely what is done with that element *is* important.

Separating the concern of "how to grab an element" from "what to do with it" thus makes more sense than separating the concern of "interacting with HTML" from "interacting with the web page".

2. It leads to important details about the test's interaction being concealed by vague abstractions
---------------------------------------------------------------------------------------------------

The user might click, enter text, drag and drop, scroll to, etc. Whatever you do with an element *that is part of the specification*.

A clear example of this anti-pattern can be seen in [this tutorial](https://robots.thoughtbot.com/better-acceptance-tests-with-page-objects), ironically titled "how to write better acceptance tests".

The page object for "Todo" has a step "create". *How* is the todo created though? What did the mock user do while they were creating? Can you tell from the scenario? Nope. You have to dig in to the code in order to do figure out what happened. It literally just gives you the most abstract view possible, which would not be enough for the "customer" (say, the CEO of this todo-app business) to know if it did what they wanted.

Of course, this is still a tendency and it is entirely possible to create page objects that do not do this. Sadly, this is a tendency that is frequently [actively encouraged](http://aslakhellesoy.com/post/11055981222/the-training-wheels-came-off) as a "best practice".


3. The page object pattern leads to more code than is necessary
---------------------------------------------------------------

In the page object pattern every page is a class and every action is a method. If you have an application with a lot of pages and a lot of potential actions that can lead to thousands of extra lines of turing complete code to maintain.

Part of the idea behind seleniumdirector is to reduce to configuration what would otherwise be code without losing the necessary expressivity to perform all of the same actions. This means that it is not only simpler to maintain for programmers, it can potentially be maintained by non-developers.
