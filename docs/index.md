SeleniumDirector
================

SeleniumDirector is a python 3 library that makes it straightforward to write easily maintainable 
python code to interact with websites in a non-brittle way using the screenplay pattern with
selenium.

Seleniumdirector reads YAML "selector" files which associate readable labels with complex selectors
- i.e. class name selectors, id selectors, attribute selectors, text and xpath.

It requires writing a lot less python code than typical "page object pattern"
and relies largely upon configuration.

SeleniumDirector was built to be used with [HitchStory](https://hitchdev.com/hitchstory) as a means
of writing straightforward to maintain integration/browser tests, but it completely agnostic about
where it is used. It can be used in py.test, nose or unittest or it could be used to direct other forms
of automated website interaction - e.g. as a scraper.



Example
-------

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


Install
-------

.. code:: bash

  $ pip install seleniumdirector


Using SeleniumDirector
----------------------

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}



Why not X instead?
------------------

{% for dirfile in subdir("why-not").is_not_dir() - subdir("why-not").named("index.md") -%} 
- [{{ title(dirfile) }}](why-not/{{ dirfile.namebase }})
{% endfor %}
