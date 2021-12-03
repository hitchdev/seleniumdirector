{% if readme -%}
# SeleniumDirector
{%- else -%}
---
title: SeleniumDirector
---

{% raw %}
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/seleniumdirector?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/seleniumdirector">
{% endraw %}

{% endif %}


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

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


## Install with pip

```bash
$ pip install seleniumdirector
```

You can also use hitchkey to generate a skeleton project structure along
with [hitchstory](https://hitchdev.com/hitchstory/).

Either install hitchkey with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipx install hitchkey
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

{% for dirfile in (subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md"))|sort() -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.name.splitext()[0] }})
{% endfor %}


## Why not X instead?

{% for dirfile in (subdir("why-not").is_not_dir() - subdir("why-not").named("index.md"))|sort() -%}
- [{{ title(dirfile) }}](why-not/{{ dirfile.name.splitext()[0] }})
{% endfor %}



## Contributors:

- Chaitu Shantharam
