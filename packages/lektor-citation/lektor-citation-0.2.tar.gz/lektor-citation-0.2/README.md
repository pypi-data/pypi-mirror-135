# lektor-citation

An APA-styled citation plugin for the lektor static content management system (https://getlektor.com).

## Preparations

Install the plugin by
```
lektor plugin add lektor-citation
```

or by copying this repository into the _packages_-folder of your lektor-project.

Create an _citation.ini_ in its _configs_-folder:
```
[Bibtex]
file = Literature.bib
```

And put a _Literature.bib_ BibTex-file into the project's _assets_-folder respectively.

## Jinja_env

### Bibliography
To get a formated output of your whole BibTex library you can either
1. Use method citation\_short\_output in the template of your literature page. It creates an unordered list of entries.
```
  <ul id="literatur">
  {% for entry in citation_entries() %}
  {{ citation_short_output(entry)|decode|safe }}
  {% endfor %}

</ul>
```
2. Use method citation\_full\_output instead. This creates a more complete html-output for every entry.
```
  {% for entry in citation_entries() %}
  {{ citation_full_output(entry)|decode|safe }}
  {% endfor %}
```
produces
```
<h2>{title}</h2><h3>{authors} ({pubYear})</h3>
<p>{note}</p>
<dl class="literature">
<dt class="edition"></dt>
<dd>{edition}</dd>
<dt class="editors"></dt>
<dd>{editors}</dd>
<dt class="pages"></dt>
<dd>{pages}</dd>
<dt class="issbn"></dt>
<dd>{issbn}</dd>
<dt class="publisher"></dt>
<dd>{publisher}</dd>
</dl>
```
3. You may also use the citation\_entry method in combination with [pybtex*s __Entry__-class](https://docs.pybtex.org/api/parsing.html#pybtex.database.Entry). For example:

```
<ul>
  {% for entry in citation_entries() %}
<li>{{ citation_entry(entry).fields['title'] |decode }}</li>
  {% endfor %}
  </ul>
```
This creates an unordered list of all the titles of your bibtex file.
Of course you can also use citation\_entry without a loop and put any id of your bibtex entries into it as parameter.

Alternatively to the pybtex methods you can use the following **jinja_env globals**:

    citation_authors_short(entry)
    citation_authors_full(entry)
    citation_editors_short(entry)
    citation_editors_full(entry)
    citation_pubYear(entry)
    citation_edition(entry)
    citation_publisher(entry)
    citation_title(entry)
    citation_url(entry)
    citation_issbn(entry)
    citation_pages(entry)
    citation_note(entry)
        
### In-text Cites
To cite a certain entry in your texts you can use the **jinja_env globals**:

	citation_full_cite(id, link="")
	citation_full_citeNP(id, link="")
	
Both methods create a complete hyperlink inside your text for the entry with _id_. You may give it any url to the _link_ parameter to e.g. link it to your bibliography page. The NP in the second stands for _No Parantheses_. So you'll receive e.g.

	AuthorI & AuthorII (2019)
or
	
	(AuthorI & AuthorII, 2019)
	
Thanks to the **lektor-jinja-content** plugin which is a dependency of this plugin you might also use the globals inside your markdown or html contents, too.
