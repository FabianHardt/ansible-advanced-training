# Hashicorp Vault Demo [instructor only]


## Setup Hashicorp Vault 
- run container: 
    ```bash
    $ docker run --cap-add=IPC_LOCK -e 'VAULT_LOCAL_CONFIG={"listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' -p 8200:8200 --name=hashi-vault hashicorp/vault server`
    ```
    
- Vault GUI will be accessible under `http://127.0.0.1:8200/ui/`. Open an SSH Tunnel to access with a browser. Remember that docker ports listen on 127.0.0.1 only (and not on public IP!).

- (on first run) unseal vault and copy *root token* and unseal *key(s)* to a safe place
- (on container restart) unseal vault and enter using root token

- create a KV secret engine and create a secret with at least the following keys: `somesecretkey`, `anothersupersecretkey`

## Running the demo
Copy the root token into the playbook as `vault_token:` variable.

```bash
$ ansible-playbook -v vault_1.yml 
```

> #### Troubleshooting
> If you get this error, install HVAC library:
> ```
> localhost | FAILED! => {
>     "msg": "An unhandled exception occurred while running the lookup plugin 'hashi_vault'. Error was a <class 'ansible.errors.AnsibleError'>, original message: Please pip install hvac to use the hashi_vault lookup module.. Please pip install hvac to use the hashi_vault lookup module."
> }
> ```
> 
> Install HVAC:
> ```bash
> $ pip install hvac
> ```
