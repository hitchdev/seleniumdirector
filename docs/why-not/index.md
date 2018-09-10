---
title: Why not X?
---

{% for dirfile in thisdir.is_not_dir() - thisdir.named("index.md") -%}
- [{{ title(dirfile) }}]({{ dirfile.namebase }})
{% endfor %}

If you'd like to write or link to a rebuttal to any argument raised
here, feel free to raise a ticket.
