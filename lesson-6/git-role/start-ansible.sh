#!/bin/bash

ansible-galaxy install -r requirements.yml
ansible-playbook site.yml -v
