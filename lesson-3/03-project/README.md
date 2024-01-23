Hands-on project - 1 - install Docker
=====================================

**Read the following instructions from the original `docs.docker.com` website to get an idea what tasks have to be accomplished by an Ansible play for installing Docker on the target host. Which modules could be useful?**

>## Install Docker Engine using the apt repository
>
>Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.
>
>### Set up Docker's apt repository.
>
>```bash
># Add Docker's official GPG key:
>sudo apt-get update
>sudo apt-get install ca-certificates curl gnupg
>sudo install -m 0755 -d /etc/apt/keyrings
>curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
>sudo chmod a+r /etc/apt/keyrings/docker.gpg
>
># Add the repository to Apt sources:
>echo \
>    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
>    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
>    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
>sudo apt-get update
>```
>> **Note**  
>> If you use an Ubuntu derivative distro, such as Linux Mint, you may need to use UBUNTU_CODENAME instead of VERSION_CODENAME.
>
>### Install the Docker packages.
>
>To install the latest version, run:
>```bash
>sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
>```
>
>Verify that the Docker Engine installation is successful by running the hello-world image.
>```bash
>sudo docker run hello-world
>```
>This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.
>
>You have now successfully installed and started Docker Engine.

## Exercise 🖐
- **Write a play to install docker as described in the instructions above!**
- **Finish the play with a task that runs the *hello-world* image.**

Here is a list of modules that could come in handy:
- `ansible.builtin.get_url` - downloads files from HTTP, HTTPS, or FTP to the remote server
- `ansible.builtin.apt` - manages apt-packages
- `ansible.builtin.apt_repository` - add or remove an apt-repository in Ubuntu and Debian
- `ansible.builtin.command` - the given command will be executed on all selected nodes
- `ansible.builtin.shell` - similar to *ansible.builtin.command* but runs the command through a shell (`/bin/sh') on the remote node
- `ansible.builtin.set_fact` - allows setting variables associated to the current host
- `ansible.builtin.debug` - output a message or a variable's value

> **Of course** the easy way out is to put the whole installation script above into a single *shell* task.  
> Try to avoid that for the excercise's sake! ;)


## Hints
- start writing a *play* in a *playbook* (a yaml file, say, `docker_execise.yml`)
    ```yaml
        ---
        - name: <useful namo of this play>
          hosts: <where to execute - see static inventory file>
          tasks: 
            - name: task 1
              <(fully qualified) module-name>
                <module-parameters>
            - name: task 2
            ...
    ```
- lookup necessary documentation on the modules with `ansible-doc <module name>`
- try to figure out which task can be executed by a native Ansible module and which ones would be better suited for the `command` or `shell` module
- *since Ansible modules are quite powerful they can sometimes take more than one step at a time, e.g. have a look at the* update_cache *parameter*
- shell expressions can be hard to read:
    - `$(. /etc/os-release && echo "$VERSION_CODENAME")` reads the file /etc/os-release as shell-source and makes the variables defined inside this file available to the environment; then variable $VERSION_CODENAME is echoed:  
        ```bash 
            $ . /etc/os-release && echo $VERSION_CODENAME
            jammy
        ```
    - `$(dpkg --print-architecture)` simply calls the dpkg tool 
        ```bash
            $ dpkg --print-architecture
            amd64
        ```
- `curl` won't be necessary
- for some changes on the target host *root access* is required - how do we become root?
- **before** running the playbook make sure you edited the static hosts inventory file and entered the VM hostname that was assigned to you: `oc-ansible-schulung-<NAME>.centralus.cloudapp.azure.com`, where <NAME> is `s` + your user number: s01, s02, ..., s017.
- run playbook with `ansible-playbook -i hosts -v docker_excercise.yml`

```





```
*If you are stuck you may peek at the solution in `install_docker.yml`.*

