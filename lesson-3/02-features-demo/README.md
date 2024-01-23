# Demo 1 - Elevation / `become` 🖐

```bash
  ansible-playbook -i hosts 08-feature_become.yml
```
Playbook creates a user, becomes this user to print a message and deletes it again.


<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

# Demo 2 - polling 🖐

```bash
  ansible-playbook -i hosts 09-feature_polling.yml -v
```

**Remember** to apply the `-v` parameter to see whats going on behind the scenes!

