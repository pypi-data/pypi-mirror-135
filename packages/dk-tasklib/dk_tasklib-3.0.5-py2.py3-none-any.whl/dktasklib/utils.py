# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import string
import sys
from contextlib import contextmanager

from dkfileutils.path import Path
import operator

join = os.path.join
null = "NUL" if sys.platform == 'win32' else '/dev/null'
win32 = sys.platform == 'win32'


class Column(dict):
    pass


# from dkbuild/utils/tableprinter.py
def format_table(data, *columns, **kw):
    """Format data into a .rst-like formatted table.

       Args:
           data: list of dict/object (having fields corresponding to `columns`)
           columns: one-or-more

                 dict(title='',
                      field='',
                      align='left',
                      format=lambda x:x)

               title is optional and defaults to field, other defaults as
               indicated.
           kw[get_field]: function to extract fields from data objects, ie.:
               ``get_field(data[i], columns[i]['field']) => data[i].field``
               Default value is :func:`operator.itemgetter`

       Usage::

           >>> print format_table(
           ...     [
           ...         dict(field1=42, field2='world', field3='n/a'),
           ...         dict(field1=12, field2='hello')
           ...     ],
           ...     Column(field='field1', format=str, align='center'),
           ...     Column(field='field2', title='f2           ', align='right')
           ... )
           ====== =============
           field1 f2
           ====== =============
             42           world
             12           hello
           ====== =============

    """
    fields = [col['field'] for col in columns]
    titles = [col.get('title', col['field']) for col in columns]
    identity = lambda x: x      # noqa
    fmt = [col.get('format', identity) for col in columns]
    _align = [col.get('align', 'left') for col in columns]
    _alignselect = {'left': '', 'right': '>', 'center': '^'}
    align = [_alignselect[a] for a in _align]
    getter = kw.get('get_field', operator.itemgetter)
    get_fields = [getter(field) for field in fields]

    field_lengths = [len(t) for t in titles]
    for item in data:
        values = [fmtfn(getfn(item)) for fmtfn, getfn in zip(fmt, get_fields)]
        value_lengths = [max([0] + [len(ln) for ln in v.splitlines()]) for v in
                         values]
        field_lengths = [max(fieldval) for fieldval in zip(value_lengths,
                                                           field_lengths)]
    rst_line = ['=' * clen for clen in field_lengths]
    thead = [
        rst_line,
        ['%-*s' % (clen, title) for clen, title in zip(field_lengths, titles)],
        rst_line
    ]

    def get_lineno(n, val):
        lines = val.splitlines()
        if n >= len(lines):
            return ''
        return lines[n]

    rows = []
    for item in data:
        values = [fmtfn(getfn(item)) for fmtfn, getfn in zip(fmt, get_fields)]
        multiline = [v.count('\n') for v in values]
        if any(multiline):
            for i in range(max(multiline) + 1):
                line = [get_lineno(i, val) for val in values]
                rows.append([
                    '{:{align}{width}}'.format(value, align=a, width=w)
                    # line, align=align[i], width=field_lengths[i])
                    for a, w, value in zip(align, field_lengths, line)
                ])
        else:
            rows.append(
                ['{:{align}{width}}'.format(value, align=a, width=w)
                 for a, w, value in zip(align, field_lengths, values)]
            )
        if kw.get('rowspace'):
            rows.append(['' * len(columns)])
    if kw.get('rowspace'):
        del rows[-1]
    tfoot = [rst_line]
    header = '\n'.join([' '.join(row) for row in thead])
    body = '\n'.join([' '.join(row) for row in rows])
    footer = '\n'.join([' '.join(row) for row in tfoot])
    return '\n'.join([header, body, footer])


def dest_is_newer_than_source(src, dst):
    """Check if destination is newer than source.

       Usage::

            if not force and dest_is_newer_than_source(source, dest):
                print 'babel:', dest, 'is up-to-date.'
                return dest

    """
    if not os.path.exists(dst):
        return False
    if not os.path.exists(src):
        raise ValueError("Source does not exist: " + src)
    return os.path.getmtime(src) < os.path.getmtime(dst)


class _MissingDottedString(str):
    def __getattr__(self, attr):
        return _MissingDottedString(self[:-1] + '.' + attr + '}')


class _MissingContext(dict):
    def __missing__(self, key):
        return _MissingDottedString('{%s}' % key)


def fmt(s, ctx):
    """Use the mapping `ctx` as a formatter for the {new.style} formatting
       string `s`.
    """
    return string.Formatter().vformat(s, (), _MissingContext(ctx))


def switch_extension(fname, ext="", old_ext=None):
    """Switch file extension on `fname` to `ext`. Returns the resulting
       file name.

       Usage::

           switch_extension('a/b/c/d.less', '.css')

    """
    name, _ext = os.path.splitext(fname)
    if old_ext:
        assert old_ext == _ext
    return name + ext


def filename(fname):
    """Return only the file name (removes the path)
    """
    return os.path.split(fname)[1]


@contextmanager
def message(s):
    try:
        print((' %s ' % s).center(80, '-'))
        yield
    except:     # noqa
        print('error =====>', s, '<====== error')
        raise
    else:
        print((' (ok: %s) ' % s).center(80, '='))


@contextmanager
def env(**kw):
    """Context amanger to temporarily override environment variables.
    """
    currentvals = {k: os.environ.get(k) for k in kw}
    for k, v in kw.items():
        os.environ[k] = str(v)
    yield
    for k in kw:
        if currentvals[k] is None:
            os.unsetenv(k)
        else:
            os.environ[k] = currentvals[k]


@contextmanager
def cd(directory):
    """Context manager to change directory.

       Usage::

           with cd('foo/bar'):
               # current directory is now foo/bar
           # current directory restored.

    """
    cwd = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(cwd)


def find_pymodule(dotted_name):
    """Find the directory of a python module, without importing it.
    """
    name = dotted_name.split('.', 1)[0]
    for p in sys.path:
        pth = Path(p)
        if not pth:
            continue
        try:
            # print 'trying:', name, 'in', pth, os.listdir(pth)
            if name in pth and (pth/name).isdir():
                return pth/name
            if name + '.py' in pth:
                return pth
        except OSError:
            continue
        except Exception as e:
            print('error', pth, e)
            raise
    raise ValueError("Path not found for: " + dotted_name)
