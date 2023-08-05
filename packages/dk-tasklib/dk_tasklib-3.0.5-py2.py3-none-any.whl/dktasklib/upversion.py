# -*- coding: utf-8 -*-
"""
Update a package's version number.
"""
from __future__ import print_function
import re
import os
import textwrap
import warnings

from dkfileutils.path import Path
from dktasklib.wintask import task
from invoke import Collection
from .rule import BuildRule
from .package import Package


def files_with_version_numbers(pkg=None):
    pkg = pkg or Package()
    root = pkg.root
    default = {
        root / 'setup.py',
        root / 'package.json',
        root / 'package.ini',
        root / 'package.yaml',
        root / 'dkbuild.yml',
        root / 'docs' / 'conf.py',
        root / 'src' / 'version.js',
        root / 'js' / 'version.js',
        root / 'styles' / 'index.less',
        root / 'styles' / 'index.scss',
        root / 'less' / 'index.less',
        pkg.source / '__init__.py',
        pkg.source / '_version.py',
        pkg.source / 'package.json',
    }
    return default


def _replace_version(fname, cur_version, new_version):
    """Replace the version string ``cur_version`` with the version string
       ``new_version`` in ``fname``.
    """
    if not fname.exists():
        return False

    with open(fname, 'rb') as fp:
        txt = fp.read()

    try:
        cur_version in txt
        uc = False
    except UnicodeDecodeError:
        uc = True
        txt = txt.decode('u8')

    if cur_version not in txt:  # pragma: nocover
        # warnings.warn("Did not find %r in %r" % (cur_version, fname))
        return False
    occurences = txt.count(cur_version)
    if occurences > 2:  # pragma: nocover
        warnings.warn(
            "Found version string (%r) multiple times in %r, skipping" % (
                cur_version, fname
            )
        )
    txt = txt.replace(cur_version, new_version)

    with open(fname, 'wb') as fp:
        fp.write(txt if not uc else txt.encode('u8'))
    return 1


@task(
    autoprint=True,
    default=True,
    help=dict(
        major="update major version number (set minor and patch to 0)",
        minor="update minor version number (set patch to 0)",
        patch="(default) update patch version",
        tag="create a tag (git only)"
    )
)
def upversion(ctx, major=False, minor=False, patch=False, tag=False):
    """Update package version (default patch-level increase).
    """
    # while it may be tempting to make this task auto-tag the new version,
    # this is generally a bad idea (bumpversion did this, and it was a mess)
    pkg = Package()
    if not (major or minor or patch):
        patch = True  # pragma: nocover
    txt_version = pkg.version
    cur_version = [int(n, 10) for n in txt_version.split('.')]
    if major:
        cur_version[0] += 1
        cur_version[1] = 0
        cur_version[2] = 0
    elif minor:
        cur_version[1] += 1
        cur_version[2] = 0
    elif patch:
        cur_version[2] += 1
    new_version = '.'.join([str(n) for n in cur_version])

    changed = 0
    changed_files = []
    addlfiles = set()
    if hasattr(ctx, 'versionfiles'):
        addlfiles = {pkg.root / fname for fname in ctx.versionfiles}
    for fname in addlfiles | files_with_version_numbers():
        was_changed = _replace_version(fname, txt_version, new_version)
        changed += was_changed
        if was_changed:
            changed_files.append(fname)
    if changed == 0:
        warnings.warn("I didn't change any files...!")  # pragma: nocover
    elif tag and pkg.vcs() == 'git':
        with pkg.root.abspath().cd():
            ctx.run('git tag -a v{version} -m "Version {version}"'.format(
                version=new_version
            ))
            ctx.run('git push origin --tags')
    print("changed version to %s in %d files" % (new_version, changed))
    for fname in changed_files:
        print('  ', fname)
    return new_version


class UpdateTemplateVersion(BuildRule):
    def __call__(self, fname):
        fname = fname.format(**self.ctx)

        if not os.path.exists(fname):
            Path(self.ctx.pkg.root).makedirs(Path(fname).dirname())
            with open(fname, 'w') as fp:
                fp.write(textwrap.dedent("""
                {% load staticfiles %}
                {% with "0.0.0" as version %}
                    {# keep the above exactly as-is (it will be overwritten when compiling the css). #}
                    {% with app_path="PKGNAME/PKGNAME-"|add:version|add:".min.css" %}
                        {% if debug %}
                            <link rel="stylesheet" type="text/css" href='{% static "PKGNAME/PKGNAME.css" %}'>
                        {% else %}
                            <link rel="stylesheet" type="text/css" href="{% static app_path %}">
                        {% endif %}
                    {% endwith %}
                {% endwith %}
                """).replace("PKGNAME", self.ctx.pkg.name))

        with open(fname, 'r') as fp:
            txt = fp.read()

        newtxt = re.sub(
            r'{% with "(\d+\.\d+\.\d+)" as version',
            '{{% with "{}" as version'.format(self.ctx.pkg.version),
            txt
        )
        with open(fname, 'w') as fp:
            fp.write(newtxt)
        print('Updated {% import %} template:', fname)


ns = Collection(
    'upversion',
    upversion,
)
ns.configure({
    'force': False,
    'pkg': {
        'name': '<package-name>',
        'version': '<version-string>',
    },
})
