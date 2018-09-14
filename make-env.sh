#!/bin/bash
ansible-playbook -i ansible/prod-hosts.yml ansible/playbook.yml --ask-vault-pass
