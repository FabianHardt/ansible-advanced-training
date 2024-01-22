# Welcome to our Ansible Advanced Training

Hello everyone, let's have a great training together in the next 3 days. To do this, we will work on the following agenda.
The following basic rules / hints apply for the following 3 days:

- Unmute yourself every time to ask a question
  - There are no dumb questions
- If you need a break, just let us know
  - By chat or just tell us
- If you need some help or support from us in any lab, just let us know
- If you're not that familiar with Linux, you can find a nice cheat-sheet over here: https://cheatography.com/davechild/cheat-sheets/linux-command-line/
- Please close any VPN connections before you start working with Ansible in our lab environments
  - This is also a good idea while using the Miro board

## Let's start our training

Open the following link in your browser:
https://miro.com/app/board/uXjVN3uMiPE=/?share_link_id=343257589076

## Agenda

**--- Day 1 ---**

1. Welcome and introduction

2. Recap of Ansible basics & Ansible basic training

    1. Quiz
    2. Variable precedence
    3. Error Handling - "block, rescue", "handlers"

3. Best practices and use of modules (introduction to some common modules)
    1. `shell` vs `command`
    2. Privilege Escalation
    3. Asynchronous Actions & Polling
    4. Delegation, Local Actions

    **--- Day 2 ---**

    1. Prompts / Start with / Step
    2. File based configuration
        1. Manage configuration in files instead of command line parameters
    3. Dynamic inventory
        1. Generation of *inventory files*, their advantages and uses

4. Templates / Jinja2
    1. Syntax
    2. Hands-on exercise on *templates*
    3. Logging / Reporting (some ideas), incl. troubleshooting

5. Credential management
    1. Ansible Vault
    2. Hashicorp Vault

**--- Day 3 ---**

1. Ansible Galaxy / Collections
    1. Building generic roles & collections
    2. Hands-on exercise to create your own collection
    3. Use `meta/main.yml` and `meta/requirements.yml`
    4. optional: Dynamic groups
2. Custom plugins
    1. Create your own plugin (What types of plugins are there?)
    2. Hands-on - Create your own filter
3. Custom modules
    1. How to create your own module
    2. Best practices - *when* does it make sense to create a module?
    3. (optional) Hands-on - create your own module
4. Feedback and Conclusion
