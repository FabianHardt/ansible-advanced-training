# Demo 1 - URI (GET) 🖐
Run demo 1 by entering:
```bash
  ansible-playbook -i hosts 01-module_uri1.yml
```
There is an error! Study the output (pretty printed by the debug task).

### Excercise 🖐:
Change the URI to a valid one and repeat.
What output is now returned?

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 2 - URI (POST) 🖐
Run demo 2 by entering:
```bash
  ansible-playbook -i hosts 02-module_uri2.yml
```
- note the result.json.data output from the debug module.
- note output of "Test URI Module" task (there is none!)

Run demo again applying the `-v` parameter:
```bash
  ansible-playbook -i hosts 02-module_uri2.yml -v
```
this time there is output from the "Test URI Module" task:

```json
ok: [localhost] =>
{
    "access_control_allow_credentials": "true",
    "access_control_allow_origin": "*",
    "changed": false,
    "connection": "close",
    "content": "{\n  \"args\": {}, \n  \"data\": \" {\\\"somedifferentkey\\\": \\\"a different value\\\", \\\"key2\\\": \\\"a not so useful information\\\"} \", \n  \"files\": {}, \n  \"form\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"identity\", \n    \"Content-Length\": \"82\", \n    \"Content-Type\": \"application/json\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"ansible-httpget\", \n    \"X-Amzn-Trace-Id\": \"Root=1-65969e07-290de6006375443f3867cf92\"\n  }, \n  \"json\": {\n    \"key2\": \"a not so useful information\", \n    \"somedifferentkey\": \"a different value\"\n  }, \n  \"origin\": \"37.201.195.254\", \n  \"url\": \"https://httpbin.org/post\"\n}\n",
    "content_length": "587",
    "content_type": "application/json",
    "cookies":
    {},
    "cookies_string": "",
    "date": "Thu, 04 Jan 2024 12:01:11 GMT",
    "elapsed": 0,
    "json":
    {
        "args":
        {},
        "data": " {\"somedifferentkey\": \"a different value\", \"key2\": \"a not so useful information\"} ",
        "files":
        {},
        "form":
        {},
        "headers":
        {
            "Accept-Encoding": "identity",
            "Content-Length": "82",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": "ansible-httpget",
            "X-Amzn-Trace-Id": "Root=1-65969e07-290de6006375443f3867cf92"
        },
        "json":
        {
            "key2": "a not so useful information",
            "somedifferentkey": "a different value"
        },
        "origin": "37.201.195.254",
        "url": "https://httpbin.org/post"
    },
    "msg": "OK (587 bytes)",
    "redirected": false,
    "server": "gunicorn/19.9.0",
    "status": 200,
    "url": "https://httpbin.org/post"
}
```

In this resulting structure one can see the key `json.data` that ist being output by the debug task.

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 3 - URI (Basic Auth) 🖐
```bash
  ansible-playbook -i hosts 03-module_uri3.yml
```
- look for response from server under `response.json`
- try executing playbook with `-v`, `-vv`, and `-vvv`: what differences can you see?

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 4 - URI (Basic Auth + Ansible Vault) 🖐
```bash
  ansible-playbook -i hosts 04-module_uri4.yml
```
Encrypt any sensitive string-data with `ansible-vault encrypt_string` (you will be prompted for the string to encrypt and for the password to encrypt with):

```bash
$ ansible-vault encrypt_string \
  --ask-vault-pass \
  --stdin-name 'password' \
  --encrypt-vault-id default \
  --output -
New Vault password:
Confirm New Vault password:
Reading plaintext input from stdin. (ctrl-d to end input, twice if your content does not already have a newline)
mysecret
password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  32393233313237306264643134353438393632376635303837393231616639393232343362656634
  6537366634336337376334316362383564323838316333360a623131373730613838623232396164
  30663539653837666533313965666433323138353334323932306631636262616535303365626531
  6232386237393631330a323031663661343365616531343638303833626361636363386132333339
  3938
Encryption successful
```
> The vault-password for this demo is configured in the `/secrets/.vault-pass` file.

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 5 - GET_URL 🖐
```bash
  ansible-playbook -i hosts 05-module_get_url1.yml
```
This module gets a file from an URL and copies it to the designated destination on the target host.

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 6 - USER 🖐
```bash
  ansible-playbook -i hosts 06-module_user1.yml
```
This play demonstrates the use of module `ansible.builtin.user` to create a bunch of users on the target host.

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 7 - COMMAND 🖐
```bash
  ansible-playbook -i hosts 07-module_command1.yml
```
A demo of the `command` module. The play executes the command `uname -a` on the target host which will return a response like this:
```
Linux schulung1 6.2.0-1018-azure #18~22.04.1-Ubuntu SMP Tue Nov 21 19:25:02 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```
