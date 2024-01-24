# Exercise "motd" = motto of the day

- create two host with different OS types (docker) on the schulungX docker daemon
    - python:alpine (Alpine)
    - python:slim (Debian)
- prepare a dynamic inventory and create group `containers`
- write a play that updates the *motd* file on each host according to its OS:
    - Debian:
        ```
        This Machine is administered by Ansible.
        Diese Maschine wird von Ansible administriert.

        OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
        Kernel: {{ ansible_kernel }}
        Hostname: {{ ansible_hostname }}

        I'm watching you, Bernd!
        ```
    
    - Alpine:
        ```
        This Machine is administered by Ansible.
        Esta maquina esta administrada por Ansible.

        OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
        Kernel: {{ ansible_kernel }}
        Hostname: {{ ansible_hostname }}

        I'm watching you, Jose!
        ```
- make a backup before overwriting the old motd file!


### Hints
- start two containers either using `docker run ...` or by creating a `docker-compose.yml`
- have a look at `lesson-3/04-inventory-demo/inventory/` folder for an idea of a dynamic inventory on docker
- `ansible_os_family` may be useful
- check out available facts by running `ansible <hostname> -m setup -i <inventory>`




