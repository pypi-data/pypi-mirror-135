# -*- coding: utf-8 -*-
from string import Template


class PyTemplate(Template):
    """
    Template strings that can replace ##{PATTERN} instances.
    """
    def __init__(self, t):
        super(PyTemplate, self).__init__(t.replace(b'$', b'$$').replace(b'##{', b'${'))

    def substitute(self, *args, **kw):
        return super(PyTemplate, self).substitute(
            **{k.upper(): v for k, v in kw.items()}
        )
