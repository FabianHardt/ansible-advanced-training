# Lesson 6 - Ansible Galaxy / Collections

This section focuses on the reusability of roles. The goal is to outsource logic and make it available to other departments for use, for example.

Now we want to do some hands-on:

## Galaxy roles - demos

1. Start with generating a dummy role

   ```bash
   # just to demonstrate
   cd /tmp/
   ansible-galaxy init dummy_role
   cd dummy_role/
   # show content
   code .
   ```

2. Create / generate a new role from a custom skeleton

   ```bash
   cd /tmp/
   ansible-galaxy init --role-skeleton ~/git/MMST/Advanced-Training/ansible_advanced_schulung/FHA-Demos/galaxy-role/role_skeleton dummy_role2
   cd dummy_role2/
   # show content
   code .
   ```


Install role from Git-Repo:

```bash
# create requirements.yml
- name: dummy
  src: https://github.com/FabianHardt/ansible-role-dummy.git
  version: main

# create site.yml
---
- name: Test new role from within this playbook
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Testing role
      ansible.builtin.include_role:
        name: dummy

# optional add start script
#!/bin/bash

ansible-galaxy collection install -r requirements.yml
ansible-playbook site.yml -v

```

## Collections - demos

We start this chapter with a very short presentation in Powerpoint...

After that, we want wo see Ansible collections in action:

### Create a empty collection

```bash
# go to lesson-6 folder
cd lesson-6/

# create a new collection <namespace>.<collection>
ansible-galaxy collection init opitz.samples

# to install the collection
cd example
ansible-galaxy collection install ../opitz -p ./collections --force 
# forces the reinstallation of this collection

# add this to ansible.cfg for local development
[defaults]
collections_path = ./collection
host_key_checking = False

# create site.yml
- name: Your awesome playbook
  hosts: localhost
  gather_facts: false

  tasks:
    - name: "Include hello_world role"
      ansible.builtin.include_role:
        name: "opitz.samples.hello_world_role"
```

1. Create `hello_world_role` in our new collection (init role or by hand)
   1. add a dummy debug task in the new role
2. Show how to install the collection globally (default behaviour)

### Use a collection from a Git-Repo

To use an Ansible collection from a Git-Repo, you should use a *requirements.yml*:

```bash
# goto folder lesson-6-2
mkdir lesson-6-2
cd lesson-6-2/

# create site.yml as usual
---
- name: Test new role from within this playbook
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Testing role
      ansible.builtin.include_role:
        name: fha.dummy.testrole
        tasks_from: main.yml

# create requirements.yml
---
collections:
  - name: https://github.com/FabianHardt/ansible-collection-dummy.git
    type: git
    version: main # develop (version 1.0.1)

# optional: create a starter shell script
#!/bin/bash

ansible-galaxy collection install -r requirements.yml
ansible-playbook site.yml -v

```

### Exercise

1. Now we create a new Galaxy Collection with a role in it, which installes a webserver on your individual target VM and copies a very simple HTML Template to this machine.
2. Install this new collection locally
3. Create a playbook and inventory file, to start the playbook and run it against your individual machine

--- optional ---

### Private Ansible Galaxy

It's possible to host a private galaxy repo:

```bash
cd ~/git/MMST/Advanced-Training/galaxy
# make dev/build

make dev/up
# make dev/up_detached
# http://localhost:8000

make dev/createsuperuser
# then create token
# User: fha / PW: Hallo123

# add to ansible.cfg
[galaxy]
server_list = release_galaxy

[galaxy_server.release_galaxy]
url=http://localhost:8000
token=2845022eb3af4acc6810ae14219857e8a54f805d

# use any sample collection
ansible-galaxy collection build

# publish
ansible-galaxy collection publish ~/git/MMST/Advanced-Training/ansible_advanced_schulung/FHA-Demos/galaxy-role/fha/dummy/fha-dummy-1.0.0.tar.gz
```

This is a nice way to show the usage of a private galaxy.



### Molecule

Start with Powerpoint to explain how molecule works...

#### Install Molecule

```bash
# Prepare work with Docker in Docker
cd ~
cd runner/
cp run.sh run-did.sh
# edit run-did.sh - add column
-v /var/run/docker.sock:/var/run/docker.sock \

# start container
./run-did.sh

# manual steps - otherwise use image fabianhardt/ansible:20240124
python3 -m venv molecule-venv
source molecule-venv/bin/activate

python3 -m pip install -U "molecule[lint]"
python3 -m pip install -U requests
python3 -m pip install -U docker
python3 -m pip install molecule-plugins
apk add docker # just for watching containers

# cause the new venv is completely empty
ansible-galaxy collection install community.docker
ansible-galaxy collection install ansible.posix
```

#### Test previous collection

In the previous step we created the `opitz.samples` collection together.
Let's add molecule configs to this collection now!

```bash
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
  enabled: true
driver:
  name: docker
lint: |
  set -e
  yamllint .
  ansible-lint
platforms:
  - name: Centos8
    image: "geerlingguy/docker-${MOLECULE_DISTRO:-centos8}-ansible:latest"
    command: ""
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
  - name: Ubuntu2004
    image: "geerlingguy/docker-${MOLECULE_DISTRO:-ubuntu2004}-ansible:latest"
    command: ""
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
    pre_build_image: true
provisioner:
  name: ansible
  config_options:
    defaults:
      interpreter_python: auto_silent
      callback_whitelist: profile_tasks, timer, yaml
verifier:
  name: ansible
scenario:
  name: default
  test_sequence:
    - destroy
    - syntax
    - create
    - converge
    - verify
    - destroy

# converge.yml
---
- name: Converge
  hosts: all
  gather_facts: false

  collections:
    - opitz.samples

  tasks:
    - name: "Include hello_world role"
      include_role:
        name: "hello_world_role"

    - name: "Include print_facts role"
      include_role:
        name: "print_facts_role"

    - name: "Add sign to file /tmp/testfile.txt"
      opitz.samples.signfile:
        name: "Fabian"
        path: "/tmp/testfile.txt"
      register: signfile_result

    - name: DEBUG print signfile result
      debug:
        msg: "Changed={{ signfile_result.changed | lower }} Stat={{ signfile_result.stat | lower }} Path={{ signfile_result.path }}"

    - name: Print string to_upper
      vars:
        str_var: "Today is holiday"
      debug:
        msg: "{{ str_var | opitz.samples.opitz_to_upper }}"

# verify.yml
---
# This is an example playbook to execute Ansible tests.

- name: Verify
  hosts: all
  gather_facts: false

  tasks:
    - name: Read status of /tmp/testfile.txt
      ansible.builtin.stat:
        path: "/tmp/testfile.txt"
      register: stat_result

    - name: Check if /tmp/testfile.txt exists
      ansible.builtin.assert:
        that: stat_result.stat.exists
        fail_msg: "ERR - The file /tmp/testfile.txt does not exist"
        success_msg: "OK - The file /tmp/testfile.txt exists"

    - name: Read /tmp/testfile.txt from remote host
      ansible.builtin.slurp:
        src: /tmp/testfile.txt
      register: file_content_slurp

    - name: Check the content of file /tmp/testfile.txt
      vars:
        file_content: "{{ file_content_slurp['content'] | b64decode }}"
      ansible.builtin.assert:
        that:
          - file_content is match("SIGNATURE:")
          - file_content is search("Hello World from opitz/samples collection")
        fail_msg: "ERR - Content of the file /tmp/testfile.txt is incorrect ({{ file_content }})"
        success_msg: "OK - The content of the file is correct"

```

After this configuration we can start the test:

```bash
# go into collection folder
molecule test
# molecule create
# molecule converge
```

