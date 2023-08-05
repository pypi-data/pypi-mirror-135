# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

from dkfileutils.path import Path


def line_endings(fname):
    """Return all line endings in the file.
    """
    _endings = {line[-2:] for line in open(fname, 'rb').readlines()}
    res = set()
    for e in _endings:
        if e.endswith(b'\r'):
            res.add(b'\r')
        elif e.endswith(b'\r\n'):
            res.add(b'\r\n')
        elif e.endswith(b'\n'):
            res.add(b'\n')
    return res


def chomp(s):
    """Remove line terminator if it exists.
    """
    if s[-2:] == b'\r\n':
        return s[:-2]
    if s[-1:] == b'\r' or s[-1:] == b'\n':
        return s[:-1]
    return s


def fix_line_endings(fname, eol=b'\n'):
    """Change all line endings to ``eol``.
    """
    lines = [chomp(line) for line in open(fname, 'rb').readlines()]
    with open(fname, 'wb') as fp:
        for line in lines:
            fp.write(line + eol)


def copy(ctx, source, dest, force=False):
    """Copy ``source`` to ``dest``, which can be a file or directory.
    """
    # print "COPY:", locals()
    # print "COPY:", ctx.force, ctx.verbose
    if source == dest:
        return dest

    source = os.path.normcase(os.path.normpath(str(source)))
    dest = os.path.normcase(os.path.normpath(str(dest)))
    flags = ""
    if sys.platform == 'win32':
        if force:
            flags += " /Y"
        # print 'copy {flags} {source} {dest}'.format(**locals())
        ctx.run('copy {flags} {source} {dest}'.format(**locals()))
    else:  # pragma: nocover
        if force:
            flags += " --force"
        ctx.run('cp {flags} {source} {dest}'.format(**locals()))
    return dest


def concat(ctx, dest, *sources, **kw):
    force = kw.pop('force', False)      # noqa
    placement = Path(dest).dirname()
    placement.makedirs()

    with open(dest, 'w') as out:
        print("Opened:", dest, "for writing.")
        for s in sources:
            with open(s, 'r') as inp:
                print("  appending:", s)
                out.writelines(inp.readlines())
        out.write('\n')

    # flags = ""
    # if sys.platform == 'win32':
    #     if force:
    #         flags += " /Y"
    #     source = '+'.join(sources)
    #     source = source.replace('/', '\\')
    #     ctx.run('copy {flags} {source} {dest}'.format(**locals()))
    # else:  # pragma: nocover
    #     if force:
    #         pass
    #         # flags += " --force"
    #     source = ' '.join(sources)
    #     # print 'cat {flags} {source} > {dest}'.format(**locals())
    #     ctx.run('cat {flags} {source} > {dest}'.format(**locals()))

    fix_line_endings(dest)
    # if len(line_endings(dest)) > 1:
    #     fix_line_endings(dest)

    return dest
