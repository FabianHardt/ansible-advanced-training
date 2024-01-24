# Lesson 5 - Credential management
[[_TOC_]]

## Ansible Vault
Ansible vault provides a way to encrypt and manage sensitive data such as passwords rather than leaving it visible as plaintext in playbooks or roles. To use Ansible Vault you need one or more passwords to encrypt and decrypt content.  Use the `ansible-vault` command-line tool to create and view encrypted variables, create encrypted files, encrypt existing files, or edit, re-key, or decrypt files. You can then place encrypted content under source control and share it more safely.

### Manage Vault passwords
With Ansible Vault one or more passwords can be used to encrypt sensitive data. Even in the same playbook we can use multiple passwords.<br/>
To differentiate passwords from another, vault IDs are needed. A vault ID can be used in the following ways:
- pass it to `ansible-vault` via `--vault-id` parameter (to create encrypted content)
- include it wherever the password for that vault ID is stored
- pass it to the `ansible-playbook` command when running a playbook that contains encrypted data

The encrypted content will be labeled with a hint on which password was used:
```yaml
my_encrypted_var: !vault |
          $ANSIBLE_VAULT;1.2;AES256;dev
          306132336334613438376538336663336430616365613033383736613138383335656536353
```
Here `dev`, the last element before the encrypted content, is the label.

The encrypted content can be linked to the matching password on the command line by providing a *source*:
```
--vault-id label@source
```
Alternatively use `--vault-password-file` to either set a path to a file containing one or more passwords, or `--ask-vault-pass` to enter it interactively.

 The `--vault-id` option works with any Ansible command that interacts with vaults, including `ansible-vault`, `ansible-playbook`, and so on.

> **Be aware** that  it is possible to use different passwords with the same vault ID label!

In default mode Ansible decrypts any content with the provided password regardless of the vault ID. To have Ansible encrypt only those secrets that posess the matching label, set `DEFAULT_VAULT_ID_MATCH` to enabled in the configuration. 

###### Available vault ID sources

- `@prompt` - prompts for the password interactively, e.g. `--vault-id dev@prompt` will prompt for the *dev* password, while `--vault-id @prompt` (without label) has the same effect as `--ask-vault-pass`
- `@path/to/file` - will retrieve the password from the given file (see below). Example: `--vault-id dev@password_file`
- `@client_script.py` - will retrieve the password by calling the given script, e.g. `--vault-id dev@somescript-py` See below.

#### Storing passwords in files
To store a vault password in a file, enter the password as a string on a single line in the file.<br/> There can always only be **one** password in a password file! If you need more passwords, create more files.

Do not add password files to source control.

#### Storing passwords in 3rd-party tools
 If you store your passwords in a third-party tool, you need a vault password client script to retrieve them from within Ansible.

When running a playbook that uses vault passwords stored in a 3rd-party tool, the client script has to be specified as the source within the `--vault-id` flag. For example:
```bash
ansible-playbook --vault-id dev@contrib/vault/vault-keyring-client.py
```

### Encrypting content
What content can be encrypted?
  - **variables**<br/>
    In an otherwise plain text file, only the value of a variable is encrypted. It is decrypted on demand, i.e. when a variable is "read".
  - **files**<br/>
    The entire file is encrypted and will be decrypted when loaded. Any structured data file can be encrypted.

#### Encrypting Variables
Variables are encrypted by the `ansible-vault encrypt_string` command.
```bash
# ansible-vault encrypt_string <password_source> '<string_to_encrypt>' --name '<string_name_of_variable>'
ansible-vault encrypt_string \
    --vault-password-file a_password_file \
    --encrypt-vault-id default \
    'foobar' \
    --name 'the_secret'
```
> **Note:** `--encrypt-vault-id` seems to be a required option now. In doubt pass "default" as argument.
```bash
the_secret: !vault |
    $ANSIBLE_VAULT;1.1;AES256
    62313365396662343061393464336163383764373764613633653634306231386433626436623361
    6134333665353966363534333632666535333761666131620a663537646436643839616531643561
    63396265333966386166373632626539326166353965363262633030333630313338646335303630
    3438626666666137650a353638643435666633633964366338633066623234616432373231333331
    6564
```

Or, using a vault ID:
```bash
# prepare a dummy password file
$ echo 'a_password' > a_password_file

# encrypt_string with password file
$ ansible-vault encrypt_string \
    --vault-id dev@a_password_file \
    --encrypt-vault-id dev \
    'foooodev' \
    --name 'the_dev_secret'
```
```bash
Encryption successful
the_dev_secret: !vault |
          $ANSIBLE_VAULT;1.2;AES256;dev
          34633763363133306539383661653363376533323362306633356337613632646232313363313166
          3236653030663635653364346134353835396238643839320a313833336166633431376535363731
          65333731393335613639356365336465356538646463616134393861303762633139333233316633
          6361313438663033630a356137613535616364616362656331393330323263323165383961353936
          3736
```

##### Viewing encrypted variables
You can view the decrypted content of a variable using the *debug* module:
```bash
$ ansible localhost -m ansible.builtin.debug -a var="the_dev_secret" -e "@vars.yml" --vault-id dev@a_password_file
```
```
localhost | SUCCESS => {
    "the_dev_secret": "foooodev"
}
```

#### Encrypting files

Ansible Vault can encrypt any structured data file used by Ansible, including:

- group variables files from inventory
- host variables files from inventory
- variables files passed to ansible-playbook with `-e @file.yml` or `-e @file.json`
- variables files loaded by `include_vars` or `vars_files`
- variables files in roles
- defaults files in roles
- tasks files
- handlers files
- binary files or other arbitrary files

The full file is encrypted in the vault.

**Example:**

```bash
$ ansible-vault encrypt plain.yml --ask-vault-pass --encrypt-vault-id default
```

Editing the file (will open in default editor):

```bash
$ ansible-vault edit plain.yml --ask-vault-pass
```



## Hashicorp Vault

Vault *secures, stores, and tightly controls access to tokens, passwords, certificates, API* keys, and other secrets critical in modern computing. Vault provides encryption services that are gated by authentication and authorization methods.

Docker Image: https://hub.docker.com/r/hashicorp/vault

`$ docker run --cap-add=IPC_LOCK -e 'VAULT_LOCAL_CONFIG={"listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' -p 8200:8200 --name=hashi-vault hashicorp/vault server`

Required Python module *hvac* for 'runner': `pip install hvac` 

Example ad-hoc usage:

```bash
$ ansible localhost -m debug -a msg="{{ lookup('hashi_vault', 'secret=/kv/data/test:somesecretkey token=hvs.s0MJAQILxeYPPv5QUZW0aWca  url=http://172.17.0.1:8200') }}"
```

```
localhost | SUCCESS => {
    "msg": "111222333444555"
}
```

Example of reading an API key from vault and writing it into a config-file:

```yaml
---
- name: Hashicorp Vault example
  hosts: all
  gather_facts: false
  tasks:
    - name: Ensure API key is present in config file
      no_log: true
      ansible.builtin.lineinfile:
        path: /etc/app/configuration.ini
        line: "API_KEY={{ lookup('hashi_vault', 'secret=config-secrets/data/app/api-key:data token=s.FOmpGEHjzSdxGixLNi0AkdA7 url=http://localhost:8201')['key'] }}"
```



**Ansible Hashicorp Vault Module Reference**

https://galaxy.ansible.com/ui/repo/published/community/hashi_vault/docs/


# Demo - Hashicorp Vault (instructor only)
- see `lesson-5/01-hashicorp-vault-demo/README.md`

