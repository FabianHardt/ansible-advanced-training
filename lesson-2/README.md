# Recap of the Ansible Basic Training

1. Start with Quiz in Menti (Link in Miro)
2. Ask if there are special points of interests
3. Variable precedence
4. Error handling



### 3. Variable precedence

Here I use the sample from last training, but start with a new, empty project.
Overwrite variables various times :-)

```bash
# Example interactive
docker run --name test1 -it geerlingguy/docker-ubuntu2204-ansible bash
docker run --platform linux/x86_64 --name test2 -it geerlingguy/docker-centos8-ansible bash

# Start only command
docker run --name test1 -d geerlingguy/docker-ubuntu2204-ansible tail -f /dev/null && docker run --platform linux/x86_64 --name test2 -d geerlingguy/docker-centos8-ansible tail -f /dev/null

ansible-playbook site.yml -v -i hosts
# 1 just with debug and inline default in it
# 2 normal role default
# 3 role var in vars folder
# 4 add to group_vars/all.yml
---
test_var: I'm a all.yml group var

# 5 add to containers group var
---
test_var: "I'm a group_var from containers.yml"

# 6 add to host_vars/test1.yml
---
test_var: "I'm a var from host_vars for host1"

# 7 vars section in play
  vars:
    test_var: This is the vars section in the play
    
# 8 play var from file
  vars_files:
    - vars/file.yml
    
# 9 directly passed to role
    - role: testrole
      test_var: This is the value passed to the role in the play

# 10 set_fact (add this to role tasks)
- name: Dynamically set facts
  ansible.builtin.set_fact:
    test_var: "I'm dynamically set by set_fact"

# 11 dynamic vars include (add to main.yml)
- name: Load a variable file based on the OS type, or a default if not found.
  ansible.builtin.include_vars: "{{ item }}"
  with_first_found:
    - '{{ ansible_distribution }}.yml'
    - '{{ ansible_os_family }}.yml'
    - default.yml

# 11.1 comment set_fact - to see dynamic include_vars
         -> learning: tasks order is not important 

# 12 include role param (site.yml)
  tasks:
    - name: Including role testrole
      ansible.builtin.include_role:
        name: testrole
      vars:
        test_var: "I'm an include role param"

# last ansible-playbook site.yml -v -i hosts -e test_var=command-line

docker rm test1 && docker rm test2
```



### 4. Error handling

First show this, as a bad example:

(copy in text editor)

```bash
# Dummy sample - just ignore errors
ansible-playbook playground-01.yml -v

# Rescue Blocks
ansible-playbook playground-02.yml -v
ansible-playbook site.yml -v # Uncomment

# Ignore unreachable hosts
ansible-playbook playground-03.yml -v -i inventory

# Error behaviour with multiple hosts
docker run --name test1 -it geerlingguy/docker-ubuntu2004-ansible bash
docker run --name test2 -it geerlingguy/docker-ubuntu2004-ansible bash

ansible-playbook playground-04.yml -v -i inventory

docker rm test1 && docker rm test2
```

