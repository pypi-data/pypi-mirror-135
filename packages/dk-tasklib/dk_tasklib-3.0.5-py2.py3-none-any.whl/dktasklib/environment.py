"""
Global state.
"""


class Environment(object):
    def __call__(self, ctx):
        return ctx


env = Environment()
