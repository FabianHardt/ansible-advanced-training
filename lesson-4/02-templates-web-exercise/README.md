Hands-on Templating 🖐
=====================

## Exercise Description
In this exercise e want to 
- create a template that will dynamically generate a HTML file. 
- This file should go into the `/tmp/` directory of the *app2* service container that we created earlier.
- Call the webserver on that container with `curl <docker_host>` to see if it worked.

## Preliminaries
We should start the services first and put a default *index.html* into the webserver's docroot folder:

```bash
$ ansible-playbook -v -i inventory/ 01-start_docker_services.yml
```

> You could run `docker compose -p example ps` on the *target host* to see if the services started.

## Templating
Expand the Jinja2 Template under `roles/demo/templates/demo_template.j2` to fit the following requirements:

- show a *`<h1>`* headline templated from variable `headline`
- show an introductory text as paragraph (*`<p>`*) from variable `intro`
- show a list of participants, e.g. the first names of your fellow training class members<br/>
  (use HTML tags `<ol><li></li>...</ol>`, with list items generated by a for-loop)
- use a variable `me` to identify your own name and highlight it in the previous list, e.g. by using `<em>` or `<b>` tags

When done templating run the playbook with `-vvv`:
```bash
$ ansible-playbook -vvv -i inventory/ 02-templated_web_exercise.yml
```

Watch the result by calling `curl <docker_host>` again.

#### Hint
To accelerate the templating task, you could write a short play that templates the `j2` file to a variable and print out the variable via a debug task.


