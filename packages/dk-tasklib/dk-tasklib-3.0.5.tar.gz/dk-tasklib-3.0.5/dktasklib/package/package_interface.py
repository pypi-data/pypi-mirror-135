# -*- coding: utf-8 -*-
import json
# import pprint
from configparser import RawConfigParser

import invoke
from dkfileutils.pfind import pfind as _pfind
from dkfileutils.path import Path
# from dkfileutils.changed import Directory
from invoke.config import Config
from dkpkg import Package as DKPKGPackage


def pfind(path, *fnames):
    res = _pfind(path, *fnames)
    return Path(res) if res is not None else None


class Package(DKPKGPackage):
    overridables = DKPKGPackage.KEYS | {'version'}

    def overrides(self, **res):
        setup_py = pfind('.', 'setup.py')
        if setup_py:
            root = setup_py.dirname()
            with root.abspath().cd():
                res['version'] = self.ctx.run(
                    'python setup.py --version',
                    hide=True
                ).stdout.strip()

        res.update(self._read_dkbuild_ini())

        package_json = pfind('.', 'package.json')
        if package_json:
            # root = package_json.dirname()
            with open(package_json, 'r') as fp:
                pj = json.load(fp)
                for k, v in pj.items():
                    if k in Package.overridables:
                        res[k] = v

        return res

    def _read_dkbuild_ini(self):
        dkbuild_ini = pfind('.', 'dkbuild.ini')
        if not dkbuild_ini:
            return {}
        cp = RawConfigParser()
        cp.read(dkbuild_ini)
        return dict((k, v) for k, v in cp.items('dkbuild')
                    if k in Package.overridables)

    def __init__(self, ctx=None):
        self.ctx = ctx or invoke.Context()
        pkgdir = pfind('.',
                       'setup.py',
                       'dkbuild.ini',
                       'package.json')
        if pkgdir is None:
            raise IOError("Didn't find setup.py|dkbuild.ini|package.json in "
                          "any parent directory up to, and including root.")
        root = pkgdir.dirname()
        ispkg = 'setup.py' in root
        overrides = self.overrides() if ispkg else self.overrides(source=root)
        super(Package, self).__init__(root, **overrides)

    def vcs(self):
        """Return the name of the version control system handling this package.
        """
        if (self.root / '.svn').exists():
            return 'svn'
        elif (self.root / '.git').exists():
            return 'git'
        elif (self.root / '.hg').exists():
            return 'hg'
        else:
            return ''

    # invoke'ism?
    def config(self):  # pragma: nocover
        cfg = Config(dict(iter(self)))
        cfg.name = self.name
        cfg.root = self.root
        cfg.source = self.source
        cfg.docs = self.docs
        cfg.django_static = self.django_static
        return cfg

    def __repr__(self):
        return self.__class__.__name__
        # return pprint.pformat(self.config())

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(str(e))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self):
        return iter([])
