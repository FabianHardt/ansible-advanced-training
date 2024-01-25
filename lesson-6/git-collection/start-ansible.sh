#!/bin/bash

ansible-galaxy collection install -r requirements.yml
ansible-playbook site.yml -v
