Dynamic Inventory with Ansible
==============================

## Prerequisites: configure Docker
This step is to enable the Docker daemon on the target host to communicate via TCP port 2375.
```bash
$ ansible-playbook -i hosts 01-configure_docker.yml
```
If something goes wrong, try to troubleshoot by conntecting via ssh to the target host and run `sudo systemctl status docker` and `sudo journalctl -u docker.service` to get some insights.

## Preprare some targets
In order to see something, we have to prepare some dummy target hosts that will appear in our dynamic inventory. After finishing the excercise *project* you should have docker and docker compose installed on the target host "schulungX".  

First we will copy a `docker-compose.yaml` to the target host and create a project infrastructure based on it. Note that it is not necessary (yet) to start any containers - just creating the project with its service containers will do. 

```bash
$ ansible-playbook -i hosts 02-start_docker_servies.yml
```

<br/>
<br/>
<br/>

---
## Hands-on! 🖐 [⏱ 10']
- **run the two playbooks as described above!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


## Dynamically generated Inventory
The inventory of this demo is configured to connect to the Docker daemon on the target host. From the metadata returned it will construct the configured inventory.<br/>
Have a look at the `inventory/` folder where two files are located: `hosts`, a statically configured inventory file (actually the same we used so far in the other demos) and `docker.yaml`:
```yaml
# Minimal example using remote Docker daemon
plugin: community.docker.docker_containers
docker_host: tcp://oc-ansible-schulung-ibr.centralus.cloudapp.azure.com:2375
verbose_output: false
debug: true
strict: true

# keyed_groups:
#   - key: docker_config.Labels['com.example.department']
#     prefix: 'label'
#     parent_group: docker
#   - key: docker_config.Labels['com.example.type']
#     prefix: 'label'
#     parent_group: docker

# groups:
#   busyboxes: (docker_config['Image'] is defined and 'busybox' in docker_config['Image'])
#   alpines: (docker_config['Image'] is defined and 'alpine' in docker_config['Image'])
#   finance: (docker_config['Labels']['com.example.department'] is defined and 'Finance' in docker_config['Labels']['com.example.department'])
```
The keyword `plugin` is the only required one by the *auto*-inventory plugin. It identifies the name of the plugin to call and passes this configuration to it. The specified plugin `community.docker.docker_containers` comes with its own requirements. `docker_host` is the host that will be queried. Note that TCP connection is not enabled by default (we did this in the *configure_docker* step) and there should be no firewall restriction to communicate with this port, either.

The `debug:` and `strict:` options are - as **best practice** - set to `true` when developing the inventory; in *production* they should be set to `false`.

Check inventory before project creation:
```bash
$ ansible-inventory -i inventory/ --graph
@all:
  |--@schulung:
  |  |--schulung1
  |--@ungrouped:
  |  |--localhost
```
> **Note:** If you get an error running `ansible-inventory` in the runner, there may be the Docker Python SDK missing. 
> Install it with `pip install docker`.

> **Note:** If you get a connection error on `/var/run/docker.sock`, check if it is actually mounted to the runner.


## Hands-on! 🖐 [⏱ 3']
- **run the command as described above!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


On the Ansible controller *cd* into the *04-inventory-demo* folder and run:
```bash
$ ansible-playbook start_docker_services.yml -v
```

> **Error?**  
> If you're getting an error in terms of *`Get \"https://registry-1.docker.io/v2/\": dial tcp 127.0.0.1:443: connect: connection refused"`* then check `/etc/hosts` file on your <u>target host</u>. Probably registry-1.docker.io got mapped to 127.0.0.1 there. Remove that line and try again.


Now, run *ansible-inventory* again to see our newly created hosts:
```bash
$ ansible-inventory -i inventory/ --graph
```
```bash
@all:
  |--@schulung:
  |  |--schulung1
  |--@ungrouped:
  |  |--app1
  |  |--localhost
  |  |--web1
  |  |--web2
```

## Hands-on! 🖐 [⏱ 3']
- **run the commands as described above!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>






To get more information on these hosts, for example to be able to map these hosts into groups, run the following command on the Ansible controller:
```bash
$ ansible-inventory -i inventory/ --list
```
This command responds with a JSON structure as follows:
```json
{
  "_meta": {
    "hostvars": {
      "app1": {
        "ansible_connection": "community.docker.docker_api",
        "ansible_docker_api_version": "auto",
        "ansible_docker_docker_host": "tcp://oc-ansible-schulung-ibr.centralus.cloudapp.azure.com:2375",
        "ansible_docker_timeout": 60,
        "ansible_docker_tls": false,
        "ansible_docker_use_ssh_client": false,
        "ansible_docker_validate_certs": false,
        "ansible_host": "app1",
        "docker_name": "app1",
        "docker_short_id": "83a275989439e"
      },
      "localhost": {
        "ansible_connection": "local"
      },
      "schulung1": {
        "ansible_host": "10.1.2.5",
        "ansible_ssh_private_key_file": "~/.ssh/schulung_rsa"
      },
      "web1": {
        "ansible_connection": "community.docker.docker_api",
        "ansible_docker_api_version": "auto",
        "ansible_docker_docker_host": "tcp://oc-ansible-schulung-ibr.centralus.cloudapp.azure.com:2375",
        "ansible_docker_timeout": 60,
        "ansible_docker_tls": false,
        "ansible_docker_use_ssh_client": false,
        "ansible_docker_validate_certs": false,
        "ansible_host": "web1",
        "docker_name": "web1",
        "docker_short_id": "5b17352a85cd8"
      },
      "web2": {
        "ansible_connection": "community.docker.docker_api",
        "ansible_docker_api_version": "auto",
        "ansible_docker_docker_host": "tcp://oc-ansible-schulung-ibr.centralus.cloudapp.azure.com:2375",
        "ansible_docker_timeout": 60,
        "ansible_docker_tls": false,
        "ansible_docker_use_ssh_client": false,
        "ansible_docker_validate_certs": false,
        "ansible_host": "web2",
        "docker_name": "web2",
        "docker_short_id": "e3558c67a78b6"
      }
    }
  },
  "all": {
    "children": [
      "schulung",
      "ungrouped"
    ]
  },
  "schulung": {
    "hosts": [
      "schulung1"
    ]
  },
  "ungrouped": {
    "hosts": [
      "app1",
      "localhost",
      "web1",
      "web2"
    ]
  }
}
```

We can see the following first level keys:
- **`_meta`** - a structure to return metadata as in the deprecated `--host <hostname>` parameter of dynamic inventory scripts. With `--list` and `_meta` you get all the information in one go. The structure returns the *hostvars* settings for every found host.
- **`all`** - a default group that contains all hosts
- **`ungrouped`** - a default group that contains all target hosts currently not mapped into a group
- ***`schulung`*** - a group defined in the static *hosts* file

Going down into the structure under `_meta` we can see that *hostvars* for all hosts are listed. We could now use these to assign hosts to a group. But looking  at the available information we note that it is somewhat "sparse". To remediate set 
- `verbose_output: true` in the `inventory/docker.yaml` and 
- run `ansible-inventory -i inventory/ --list` again.

## Hands-on! 🖐 [⏱ 3']
- **run the commands as described above!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


Have a look at `lesson-3/inventory-demo/example_inventory_list.json` to see an example of the full output. We will focus on `docker_config.Labels` and `docker_config.Image` subkeys which contain for host `app1` the following data:

```json
...
"Image": "alpine:latest",
"Labels": {
    "com.docker.compose.config-hash": "41fb8f8c199ccb69feb405b09a7a7a7f076e5b57ea58b9b6aac90f49cf7a9d17",
    "com.docker.compose.container-number": "1",
    "com.docker.compose.depends_on": "",
    "com.docker.compose.image": "sha256:f8c20f8bbcb684055b4fea470fdd169c86e87786940b3262335b12ec3adef418",
    "com.docker.compose.oneoff": "False",
    "com.docker.compose.project": "example",
    "com.docker.compose.project.config_files": "/home/sysadmin/project/docker-compose.yaml",
    "com.docker.compose.project.working_dir": "/home/sysadmin/project",
    "com.docker.compose.service": "app",
    "com.docker.compose.version": "2.21.0",
    "com.example.department": "Finance",
    "com.example.description": "Accounting webapp",
    "com.example.type": "Application"
},
...
```
Note especially the labels starting with `com.example`. *We* set those in the `docker-compose.yml` under the `labels` tag to instruct docker compose to add all subsequent keys as labels on the specified *container*. 
> ***[optional]***<br/>
> We can actually inspect the labels by running `docker inspect` on the *app1* container:
> ```bash
> $ docker inspect --format='{{json .Config.Labels}}' app1
> ```
> 
> ```json
> {
>   "com.docker.compose.config-hash": "41fb8f8c199ccb69feb405b09a7a7a7f076e5b57ea58b9b6aac90f49cf7a9d17",
>   "com.docker.compose.container-number": "1",
>   "com.docker.compose.depends_on": "",
>   "com.docker.compose.image": "sha256:f8c20f8bbcb684055b4fea470fdd169c86e87786940b3262335b12ec3adef418",
>   "com.docker.compose.oneoff": "False",
>   "com.docker.compose.project": "example",
>   "com.docker.compose.project.config_files": "/home/sysadmin/project/docker-compose.yaml",
>   "com.docker.compose.project.working_dir": "/home/sysadmin/project",
>   "com.docker.compose.service": "app",
>   "com.docker.compose.version": "2.21.0",
>   "com.example.department": "Finance",
>   "com.example.description": "Accounting webapp",
>   "com.example.type": "Application"
> }
> ```


#### Keyed groups
Labels can be used for *automatic* grouping. 
- Open the  `inventory/docker.yaml` file and uncomment the key `keyed_groups` and the attached list. 

```yaml
keyed_groups:
  
  - key: docker_config.Labels['com.example.department']
    prefix: 'label'
    parent_group: docker
  
  - key: docker_config.Labels['com.example.type']
    prefix: 'label'
    parent_group: docker
```

That list defines two group types. One using the values of key `docker_config.Labels['com.example.department']` to assign groups and the second uses the key `docker_config.Labels['com.example.type']`.  
The Label `com.example.department` has only one distinct value, so there should be only one group created. However `com.example.type` sports two different values, "Application" and "Content Server", thus two different groups should appear:

```bash
$ ansible-inventory -i inventory/ --graph 
```
```bash
@all:
  |--@docker:
  |  |--@label_Application:
  |  |  |--app1
  |  |--@label_Content_Server:
  |  |  |--web1
  |  |  |--web2
  |  |--@label_Finance:
  |  |  |--app1
  |  |  |--web1
  |  |  |--web2
  |--@schulung:
  |  |--schulung1
  |--@ungrouped:
  |  |--localhost
```

## Hands-on! 🖐 [⏱ 3']
- **run the commands as described above!**

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>


#### Groups
With the `groups` keyword some conditional grouping can be achieved. 
- Open the  `inventory/docker.yaml` file and uncomment the key `groups` and the attached dictionary.  
- Comment out (disable) the the key `keyed_groups` and the attached list.

The three groups are defined by Jinja2 conditionals:
```yaml
groups:
  busyboxes: (docker_config['Image'] is defined and 'busybox' in docker_config['Image'])
  alpines: (docker_config['Image'] is defined and 'alpine' in docker_config['Image'])
  finance: (docker_config['Labels']['com.example.department'] is defined and 'Finance' in docker_config['Labels']['com.example.department'])
```
```bash
$ ansible-inventory -i inventory/ --graph 
```
```bash
@all:
  |--@alpines:
  |  |--app1
  |--@busyboxes:
  |  |--web1
  |  |--web2
  |--@finance:
  |  |--app1
  |  |--web1
  |  |--web2
  |--@schulung:
  |  |--schulung1
  |--@ungrouped:
  |  |--localhost
```
With `groups` and Jinja2 conditionals you can operate on the same input data as before but you have more control over the name of a group and over which host enters a group.

## Hands-on! 🖐 [⏱ 3']
- **run the commands as described above!**

