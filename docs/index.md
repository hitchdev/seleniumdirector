SeleniumDirector
================

SeleniumDirector is a python 3 library that makes it straightforward to write easily maintainable 
python code to interact with websites in a non-brittle way using selenium.

Seleniumdirector reads YAML "selector" files which associate readable labels with selectors - e.g.
class name selectors, id selectors, attribute selectors, etc. It requires writing a lot less python
code than typical "page object pattern" approaches and relies largely upon configuration.

SeleniumDirector was built to be used with [HitchStory](https://hitchdev.com/hitchstory) as a means
of writing straightforward to maintain integration/browser tests, but it can also be used to direct other forms
of automated website interaction.



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
