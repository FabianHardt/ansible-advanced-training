from ansible.utils.display import Display

class FilterModule(object):
    def filters(self): return {'missing_deployment': self.missing_deployment}

    def missing_deployment(self, message, pre, post, **kwargs):
        message = '[CAUTION]: ' + pre + ' ' + str(message) + ' ' + post
        Display().display(message, color='yellow', stderr=True)
        return message