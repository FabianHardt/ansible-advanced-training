# Lesson 3 - Tips, Tricks & Best Practices

[[_TOC_]]

## Modules
Ansible modules (a.k.a. "task plugins") are the code building blocks that interact with (system-) resources or execute (system-) commands. Modules are executed on the _target host_ and can be implemented in any supported programming language (usually Python or PowerShell for Windows modules).

>### _Plays_
>_Plays_ are tasks or groups of tasks that are executed on a specified target host (or group of hosts). A collection of plays in a single YAML file is called *playbook*.
>
>### _Roles_
>A _role_ is a reusable distribution format for tasks that bundle a certain functionality. You can import a role into a play where it will be executed.
>
>### _Plugins_
>_Plugins_ extend the Ansible core functions. In contrast to modules, a plugin is executed on the Ansible controller. The way how Ansible connects to the target host is realized by a _connection plugin_, for example.
>
>### _Collections_
>A _collection_ (a.k.a. Galaxy collection) is a packaging format for the distribution of playbooks, roles, modules, or plugins.
> 

### Using Modules
Modules are always called by a _task_. A _task_ is the smallest executable code block in a play:
```yaml
  - name: debug-print a variable    (1)
    ansible.builtin.debug:          (2)
      var: result                   (3)
      verbosity: 2                  (4)
```
1. The *name* of the task;<br>
   It is **good practice** to give every task in a play or role a well distinguishable name, e.g. a short description what the task will accomplish.
1. The (fully qualified) _name of the module_ to execute;<br>
   It is **good practice** to always use the fully qualified name of a module to avoid conflicts with equally named modules in different collections.
1. A _module parameter_;<br>
   See the module's documentation for a list of required and optional parameters.
1. Another _module parameter_;<br>
   Module parameters are given as YAML _hash_ (a.k.a. dictionary, object)

### Use `ansible-doc` to lookup module parameters
The command line tool `ansible-doc` can be used to lookup a modules parameters and documentation:
```bash
$ ansible-doc ansible.builtin.uri
> ANSIBLE.BUILTIN.URI    (/home/ibr/.local/lib/python3.8/site-packages/ansible/modules/uri.py)

        Interacts with HTTP and HTTPS web services and supports Digest, Basic and WSSE HTTP authentication mechanisms. For
        Windows targets, use the [ansible.windows.win_uri] module instead.

  * note: This module has a corresponding action plugin.

OPTIONS (= is mandatory):

  [...omitted...]
```
This command also shows _where_ a module is installed by showing its path in the headline (`/home/ibr/.local/lib/python3.8/site-packages/ansible/modules/uri.py`).

### Module defaults
If you frequently call the same module with the same arguments, it can be useful to define default arguments for that particular module using the `module_defaults` keyword. This keyword can be used at _play_, _block_, and _task_ level.

```yaml
- hosts: localhost
  module_defaults:
    ansible.builtin.file:
      owner: root
      group: root
      mode: 0755
  tasks:
    - name: Create file1
      ansible.builtin.file:
        state: touch
        path: /tmp/file1

    - name: Create file2
      ansible.builtin.file:
        state: touch
        path: /tmp/file2

    - name: Create file3
      ansible.builtin.file:
        state: touch
        path: /tmp/file3
```
[Example taken from Ansible documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html)

### Return Values
Ansible modules normally return a data structure that can be registered into a variable, or seen directly when output by the ansible program. Each module can optionally document its own unique return values (visible through `ansible-doc`).

See [main documentation site](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html) to view all available return values that are common to all modules. Some useful values will be listed below:
- ***failed*** | a boolean value that indicates if a task has failed or not
    ```
      failed: false
    ```
- ***invocation*** | information on how the module was invoked
    ```
     "invocation": {
        "module_args": {
            "_original_basename": "foo.txt",
            "attributes": null,
            "backup": true,
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "content": null,
            "delimiter": null,
            "dest": "./foo.txt",
            "directory_mode": null,
            "follow": false,
            "force": true,
            "group": null,
            "local_follow": null,
            "mode": "666",
            "owner": null,
            "regexp": null,
            "remote_src": null,
            "selevel": null,
            "serole": null,
            "setype": null,
            "seuser": null,
            "src": "/Users/foo/.ansible/tmp/ansible-tmp-1596115458.110205-105717464505158/source",
            "unsafe_writes": null,
            "validate": null
        }
    ```
- ***rc*** | some modules execute command line utilities or are geared for executing commands directly (raw, shell, command, and so on), this field contains ‘return code’ of these utilities.

- ***stdout*** | some modules execute command line utilities or are geared for executing commands directly (raw, shell, command, and so on). This field contains the normal output of these utilities.

<br/>
<br/>
<br/>

---
## DEMO 🖐 01-module-demo, playbooks 01-06

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## `shell` vs. `command`
The modules `ansible.builtin.command` and `ansible.builtin.shell` both can execute cli commands on the unix based target host. But it is not as simple as "executes single command" vs "executes a script" - there are certain differences to be taken into account:

  ***`command`***
  - *bypasses* the shell

  ***`shell`***
  - respects redirections and inbuilt shell functionality

### Examples
```yaml
---
- name: command module example
  hosts: all
  tasks:
    - name: check uptime
      ansible.builtin.command: uptime
      register: command_output

    - name: command output
      ansible.builtin.debug:
        var: command_output.stdout_lines
```
```yaml
---
- name: shell module example
  hosts: all
  tasks:
    - name: list file(s) and folder(s)
      ansible.builtin.shell: 'ls -l *'
      register: command_output

    - name: command output
      ansible.builtin.debug:
        var: command_output.stdout_lines
```
The following play will fail due to the missing shell environment of the command module (`*` cannot be interpreted by the `ls` command):
```yaml
---
- name: command module example with error
  hosts: all
  tasks:
    - name: list file(s) and folder(s)
      ansible.builtin.command: 'ls -l *'
      register: command_output

   - name: command output
      ansible.builtin.debug:
        var: command_output.stdout_lines
```
Basically, use the `shell` module when you need Bash features like
- file globbing (`*` or `?` wildcards in filenames)
- pipes (`|` - concatenated command calls)
- output redirection (e.g. `cat somefile > otherfile`)
- (environment-) variable expansion


### shell scripting using yaml multiline strings
It is possible to pass an entire shell script *inline* to the `shell` module by applying the yaml multiline string syntax:
```yaml
---
- name: shell module example
  hosts: localhost
  tasks:
    - name: execute a shell script
      ansible.builtin.shell: |
        set -eo pipefail
        cd /var/log
        ls -l * | grep cfg
      register: command_output
```
It is a *best practice* to set at least the `-e` option when executing shell scripts. If *pipes* are used in the script then option `-o pipefail` should also be set.


<br/>
<br/>
<br/>

---
## DEMO 🖐 01-module-demo, playbook 07

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## Privilege Escalation
Usually Ansible executes the tasks on the target host with the privileges of the user that logged in to that host - which can be defined on the command line, by config file (ansible.cfg), in a play itself, or in the inventory.
Most users do not have sufficient rights to execute administrative tasks, e.g. change a config file on /etc/ path or start a service. 

With `become` Ansible uses the existing *privilege escalation* system the target host provides. Essentially it allows to "become" another user, such as root.

```yaml
---
- name: privilege escalation example
  hosts: localhost
  tasks:
    - name: execute command as root
      ansible.builtin.command: apt-get update
      become: true

    - name: execute command as systemaccount
      ansible.builtin.command: psql -l
      become: true
      become_user: postgres
```

<br/>
<br/>
<br/>

---
## DEMO 🖐 02-feature-demo, playbook 08

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## Asynchronous Actions & Polling
By default Ansible runs tasks synchronously, holding the connection to the remote node open until the action is completed. This also means that each task blocks the next task. Playbooks support asynchronous mode and polling:

```yaml
---
- hosts: all
  remote_user: root

  tasks:
    - name: Simulate long running op (15 sec), wait for up to 45 sec, poll every 5 sec
      ansible.builtin.command: /bin/sleep 15
      async: 45
      poll: 5
```
#### Ansible Keywords `async` and `poll`
##### `poll` > 0
Using `async` with `poll` set to a positive value, as seen in the example above, Ansible will still block the next task in your playbook, waiting until the async task either completes, fails or times out.

##### `poll` = 0
To run multiple tasks in a playbook *concurrently*, use `async` with `poll` set to 0. The playbook run eventually ends without checking back on async tasks.

If you need a synchronization point with an async task, you can register it to obtain its job ID and use the async_status module to observe it in a later task. For example:
```yaml
- name: Run an async task
  ansible.builtin.yum:
    name: docker-io
    state: present
  async: 1000
  poll: 0
  register: yum_sleeper

- name: Check on an async task
  async_status:
    jid: "{{ yum_sleeper.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 100
  delay: 10
```

> ### Notes
> - When an async task completes with polling enabled (poll > 0), the temporary async job cache file (by default in `~/.ansible_async/`) is automatically removed.
> - When running with `poll: 0`, Ansible will **not** automatically cleanup the async job cache file. You will need to manually clean this up with the *async_status* module with `mode: cleanup`.
> - Using a higher value for `--forks` will result in kicking off asynchronous tasks even faster. This also increases the efficiency of polling.
> - If the value of `async:` is not high enough, this will cause the “check on it later” task to fail because the temporary status file that the `async_status:` is looking for will not have been written or no longer exist.
> - Asynchronous playbook tasks always return *changed*.


<br/>
<br/>
<br/>

---
## DEMO 🖐 02-feature-demo, playbook 09

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>




## Delegation & Local Actions
By default, Ansible gathers facts and executes all tasks on the machines that match the `hosts` line of your playbook. However, if necessary, tasks can be *delegated* to any other host by use of the `delegate_to` keyword.

```yaml
---
- hosts: webservers
  tasks:
    - name: Take out of load balancer pool
      ansible.builtin.command: /usr/bin/take_out_of_pool {{ inventory_hostname }}
      delegate_to: 127.0.0.1

    - name: Actual steps would go here
      ansible.builtin.yum:
        name: acme-web-stack
        state: latest
```

#### `local_action`
Here is the same playbook as above, but using a *shorthand syntax* for delegating to 127.0.0.1:
```yaml
---
# ...

  tasks:
    - name: Take out of load balancer pool
      local_action: ansible.builtin.command /usr/bin/take_out_of_pool {{ inventory_hostname }}

```


## Prompts, Start and Step
Interactively prompt a user for input:
```yaml
---
- hosts: all
  vars_prompt:

    - name: username
      prompt: What is your username?
      private: false

    - name: password
      prompt: What is your password?

  tasks:

    - name: Print a message
      ansible.builtin.debug:
        msg: 'Logging in as {{ username }}'
```
`private: false` makes the input data visible on the console.

With optional command line arguments playbooks can be started at determined tasks or forced to get a confirmation of the user before running the next step:
```
--start-at-task TASK_NAME
                        start the playbook at the task matching this name
--step                one-step-at-a-time: confirm each task before running

```

<br/>
<br/>
<br/>

---
## Hands-on! 🖐 write a play that...
- **prompts for input,**
- **has some tasks to skip with `--start-at-task`**
- **can be replayed step-by-step with `--step`**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>



## File based configuration
Certain settings in Ansible are adjustable via a configuration file.
Ansible will look for configuration files in the following order:

* ANSIBLE_CONFIG (an environment variable)
* ansible.cfg (in the current directory)
* .ansible.cfg (in the home directory)
* /etc/ansible/ansible.cfg

> **Ansible will process the above list and use the first file found.**  
> **Settings in files are not merged.**

The format of the configuration file is a derivative of the INI format. Comments start with a semicolon `;` (the hash-symbol `#` is also allowed when comment starts a line).

#### Generate a default `ansible.cfg`
You can generate a fully commented-out example ansible.cfg file, for example:

```bash
$ ansible-config init --disabled > ansible.cfg
```

You can also have a more complete file that includes existing plugins:

```bash
$ ansible-config init --disabled -t all > ansible.cfg
```

> **Be aware** that  Ansible will not automatically load a config file from the current working directory <u>*if the directory is world-writable*</u>. Thats a pretty common issue!

On older versions of Ansible, use `ansible-config list | more` to view available options.

#### Common configuration settings

```ini
[defaults]

; Comma separated list of Ansible inventory sources
inventory = inventories/dev/hosts  

; List of extensions to ignore when using a directory as an inventory source
inventory_ignore_extensions = .md,.j2

; Option for connections using a certificate or key file to authenticate,
; rather than an agent or passwords, you can set the default value here
; to avoid re-specifying  --private-key  with every invocation.
private_key_file = ~/.ssh/id_rsa_provisioning

; Set this to "False" if you want to avoid host key checking by the underlying
; tools Ansible uses to connect to the host
host_key_checking = False

; Sets the login user for the target machines
remote_user = root

; set the default callback plugin (task output formatting)
stdout_callback=yaml
;stdout_callback=debug
```
<br/>
<br/>
<br/>

---
## Hands-on! 🖐 Exercise Project [⏱ 45']
- **see `03-project/README.md` for instructions!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## Dynamic inventory
Dynamic inventory is useful in any non-static setup like cloud environments or when working with virtual machines. Ansible supports two ways to connect with external inventory: Inventory **plugins** and inventory **scripts**. Inventory *scripts* are *sort of deprecated*; newer installations of Ansible prefer inventory plugins. The community still supports a variety of different scripts, though: https://github.com/ansible-community/contrib-scripts/tree/main/inventory .

### Inventory plugins
Get an overview of readily available plugins on your system:
```bash
$ ansible-doc -t inventory -l
```

Most plugins use a standard YAML-based configuration file as the inventory source (passed to Ansible via the `-i` parameter). The file has only one required field `plugin:`, which should contain the name of the plugin that is expected to consume the file.

We will dig deeper into dynamic inventories in the `lesson-3/inventory-demo/README.md`.

<br/>
<br/>
<br/>

---
## DEMO 🖐 04-inventory-demo 

