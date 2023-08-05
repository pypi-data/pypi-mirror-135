# -*- coding: utf-8 -*-
from __future__ import print_function
from dktasklib.wintask import task
from .package_interface import Package
from ..utils import format_table, Column


@task
def package(ctx):
    """Print detected package directories.
    """
    pkg = ctx.pkg if hasattr(ctx, 'pkg') else Package()

    def row(attribute, value, description=''):
        return dict(attribute=attribute, value=value, description=description)

    print("The dk-tasklib Package object thinks your code has the following layout:")

    print(format_table(
        [
            row('package_name', pkg.package_name, '(repo/pip-installable name)'),
            row('name', pkg.name, '(importable name)'),
            row('root', pkg.root, '(wc)'),
            row('source', pkg.source, '(source directory)'),
            row('source_js', pkg.source_js, '(js source directory)'),
            row('source_less', pkg.source_less, '(less source directory)'),
            row('docs', pkg.docs, '(docs directory)'),
            row('django?', 'yes' if pkg.is_django() else 'no', '(django?)'),
        ],
        Column(field='attribute'),
        Column(field='value'),
        Column(field='description'),
    ))

    # keys = ['package_name', 'name', 'fname', 'root', 'source',
    #         'docs', 'django_static']
    # keylen = 1 + max(len(k) for k in keys)
    # vallen = 1 + max(len(str(getattr(pkg, k, ''))) for k in keys)
    # print
    # print '-' * keylen, '-' * vallen, '-' * (80 - keylen - vallen)
    # print 'attribute'.ljust(keylen), 'value'.ljust(vallen), 'description'
    # print '-' * keylen, '-' * vallen, '-' * (80 - keylen - vallen)
    #
    # print 'package_name'.ljust(keylen), str(pkg.package_name).ljust(vallen), '(repo/pip-installable name)'
    # print 'name'.ljust(keylen), str(pkg.name).ljust(vallen), '(importable name)'
    # print 'root'.ljust(keylen), str(pkg.root).ljust(vallen), '(root of the package/wc)'
    #
    # print 'source'.ljust(keylen), str(pkg.source).ljust(vallen), '(root of the source code)'
    # print 'source'.ljust(keylen), str(pkg.source).ljust(vallen), '(root of the source code)'
    # print 'source'.ljust(keylen), str(pkg.source).ljust(vallen), '(root of the source code)'
    #
    # print 'docs'.ljust(keylen), str(pkg.docs).ljust(vallen), '(root of documentation)'

    # if hasattr(pkg, 'is_django') and pkg.is_django():
    #     print 'django_static'.ljust(keylen), str(pkg.django_static).ljust(vallen), '(directory for static resources)'
    #
    # print '-' * keylen, '-' * vallen, '-' * (80 - keylen - vallen)
