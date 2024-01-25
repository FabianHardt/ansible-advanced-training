
#!/usr/bin/python

DOCUMENTATION = '''
---
module: samplemodule
short_description: Just a sample module
'''

EXAMPLES = '''
- name: Test our module
  samplemodule:
    name: "Fabian"
    age: 32
  register: result
'''

from ansible.module_utils.basic import *

def sample(data):
   object = {"name: ": data["name"], "age_in_days": data['age']*365}
   return object

def main():
  fields = {
		"name": {"required": True, "type": "str" },
    "age": {"required": True, "type": int},
    "mail": {"required": False, "type": "str", "default": "mail@test.de"},
	}
  module = AnsibleModule(argument_spec=fields)
  response = sample(module.params)
  module.exit_json(changed=False, result=response)

if __name__ == '__main__':
    main()
