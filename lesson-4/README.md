# Lesson 4 - Templates & Jinja2

[[_TOC_]]

- Ansible uses Jinja2 templating to enable dynamic expressions and access to variables and facts.
- All templating happens on the **Ansible control node** before the task is sent and executed on the target host.
- Templates are used by 
    - the `ansible.builtin.template` module and
    - whenever a templated expression is needed in the playbook (inline)

We have already seen the inline style of templating, whenever we wanted to pass the *value* of a variable to a task:
```yaml
    - name: jinja2 templating in task
      ansible.buildin.debug:
        msg: "This is a template: {{ varname }}"
```
In this example a variable `varname`'s value is pasted "as is" into the output string of the debug module's `msg` parameter.

### Template delimiters
There are a few kinds of delimiters. The default Jinja delimiters are configured as follows:

`{% ... %}` for Statements / Control Structures  
`{{ ... }}` for Expressions to print to the template output  
`{# ... #}` for Comments not included in the template output  

#### Control Structures
Control Structures in Jinja2 are:
- conditionals (`if`, `elif`, `else`)
- `for`-loops
- blocks

**Examples**
```jinja
{% if users %}
  users:
  {% for user in users %}
    - {{ user.name }}:
      firstname: {{ user.firstname }}
      lastname: {{ user.lastname }}
  {% endfor %}
{% else %}
  users: []
{% endif %}
```
A (filter-) block example:
```jinja
{% filter upper %}
 This test becomes uppercase
{% endfilter %}
```
Assignments:
```jinja
{% set key, value = call_something() %}
```
Includes:
```jinja
{% include 'somevardefs.yml' %}
```

<br/>

**Loop special variables**

Inside of a for-loop block, you can access some special variables:

|Variable|Description|
|--------|-----------|
|`loop.index`|The current iteration of the loop. (1 indexed)|
|`loop.index0`|The current iteration of the loop. (0 indexed)|
|`loop.revindex`|The number of iterations from the end of the loop (1 indexed)|
|`loop.revindex0`|The number of iterations from the end of the loop (0 indexed)|
|`loop.first`|True if first iteration.|
|`loop.last`|True if last iteration.|
|`loop.length`|The number of items in the sequence.|
|`loop.cycle`|A helper function to cycle between a list of sequences.|
|`loop.depth`|Indicates how deep in a recursive loop the rendering currently is. Starts at level 1|
|`loop.depth0`|Indicates how deep in a recursive loop the rendering currently is. Starts at level 0|
|`loop.previtem`|The item from the previous iteration of the loop. Undefined during the first iteration.|
|`loop.nextitem`|The item from the following iteration of the loop. Undefined during the last iteration.|
|`loop.changed(*val)`|True if previously called with a different value (or not called at all).|

Also see https://jinja.palletsprojects.com/en/3.0.x/templates/#for

#### Expressions
Reference variables using `{{ braces }}` notation.


## Filters 
With Jinja2 there exists a variery of *filters* that can be applied to the value of a variable; the syntax is as follows:

```yaml
    - name: set a variable
      ansible.builtin.set_fact:
        myvariable: "small"

    - name: jinja2 templating in playbook
      ansible.buildin.debug:
        msg: "{{ myvariable | upper }}"
```
```
localhost | SUCCESS => {
    "msg": "SMALL"
}
```

### When to put quotes around template expressions
This is a YAML-only-problem, meaning you will never have to quote anything in a pure Jija2 template file. In an Ansible playbook or role, which is implemented in YAML you may have to put quotes around expressions. Let's have a look why:
```yaml
- name: this is an Ansible task defining an empty dictionary
  ansible.builtin.set_fact:
    mydict: {}

- name: this is a task with an error
  ansible.builtin.debug:
    var: {{ mydict }}     # <= ERROR! Syntax Error while loading YAML.
```
Since you can define an empty dictionary by using shorthand notation `{}`, Ansible will always assume the beginning of a dictionary when finding an opening brace `{` at the start of a YAML value definition (i.e. behind a colon `:`). So, if you start a *value* with a Jinja2 expression `{{ foo }}`, you **must** quote the whole expression to create valid syntax!


#### List of Jinja2 builtin filters
```
abs()
attr()
batch()
capitalize()
center()
default()
dictsort()
escape()
filesizeformat()
first()
float()
forceescape()
format()
groupby()
indent()
int()
items()
join()
last()
length()
list()
lower()
map()
max()
min()
pprint()
random()
reject()
rejectattr()
replace()
reverse()
round()
safe()
select()
selectattr()
slice()
sort()
string()
striptags()
sum()
title()
tojson()
trim()
truncate()
unique()
upper()
urlencode()
urlize()
wordcount()
wordwrap()
xmlattr()
```
See [Jinja2 documentation](https://jinja.palletsprojects.com/en/latest/templates/#list-of-builtin-filters) for complete reference.

> **Filters** may be chained, e.g. `"{{ myvar | default('somedefaultvalue') | upper | replace('SOME', 'ANY') }}"` would result in `'ANYDEFAULTVALUE'` if the `myvar` variable was not set.

> **Note** that some filters name's have aliases, too, e.g. `| escape()` or `|escape` might also appear as `|e`. All aliases are described in the Jinja2 reference.


## Tests
Beside filters there are also so-called “tests” available. Tests can be used to test a variable against a common expression.  
To compose a test the verb *"is"* is added before the name of the test, e.g. `variable is defined`. Tests return boolean results `true` or `false`.  
Test may accept arguments; these two expressions are equivalent:
```jinja
{% if loop.index is divisibleby 3 %}
{% if loop.index is divisibleby(3) %}
```

#### List of Builtin Tests
```
boolean()
even()
in()
mapping()
sequence()
callable()
false()
integer()
ne()
string()
defined()
filter()
iterable()
none()
test()
divisibleby()
float()
le()
number()
true()
eq()
ge()
lower()
odd()
undefined()
escaped()
gt()
lt()
sameas()
upper()
```
See the [reference](https://jinja.palletsprojects.com/en/latest/templates/#list-of-builtin-tests) for builtin tests.


## Python Methods

You can also use any of the methods defined on a variable’s type. The value returned from the method invocation is used as the value of the expression. Here is an example that uses methods defined on *strings* (where `page.title` is a string):
```jinja
{{ page.title.capitalize() }}
```

## Global Functions
The following functions are available in the global scope by default:
```
range([start, ]stop[, step])
dict(\**items)
cycler(\*items)
joiner(sep=', ')
namespace(...)
```


<br/>
<br/>
<br/>

---
## DEMO 🖐 01-templates-demo, playbooks 01-03
- see `lesson-4/01-templates-demo/README.md` for instructions!

<br/>
<br/>
<br/>

---
## Hands-on! 🖐 02-templates-web-exercise [⏱ 30']
- see `lesson-4/02-templates-web-exercise/README.md` for instructions!

<br/>
<br/>
<br/>

---
## DEMO 🖐 03-reporting-demo
```bash
$ ansible-playbook 01-reporting.yml
```




<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

