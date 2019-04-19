import string


class HTMLFormatter(string.Formatter):
    """ Типа Jinja, но проще)) в основном для циклов """

    def format_field(self, value, spec):
        if spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        elif spec.startswith('if'):
            return (value and spec.partition(':')[-1]) or ''
        else:
            return super(HTMLFormatter, self).format_field(value, spec)