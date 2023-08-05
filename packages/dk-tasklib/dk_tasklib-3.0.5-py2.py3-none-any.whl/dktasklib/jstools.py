import os
import textwrap

from dktasklib.wintask import task
from invoke import Collection
# from dkfileutils.path import Path
from dktasklib import runners
from dktasklib.commands import Command
from dktasklib.executables import requires
from dktasklib.utils import cd, switch_extension
from dktasklib.version import copy_to_version


def ensure_package_json(ctx):
    """Is this a node package?
    """
    package_json = os.path.join(ctx.pkg.root, 'package.json')
    if not os.path.exists(package_json):
        print("Missing package.json file, creating default version..")
        with cd(ctx.pkg.root):
            ctx.run("npm init -f")
    else:
        return True


def ensure_babelrc(ctx):
    """babel needs a .babelrc file to do any work.
    """
    babelrc = os.path.join(ctx.pkg.root, '.babelrc')
    if not os.path.exists(babelrc):
        print('Misssing %s (creating default version)' % babelrc)
        with open(babelrc, 'w') as fp:
            fp.write(textwrap.dedent("""
            {
              "presets": [
                ["env", {
                  "targets": {
                    "browsers": [
                      "last 2 versions",
                      "IE >= 11"
                    ],
                    "useBuiltIns": true,
                    "node": "current"
                  }
                }]
              ],
              "ignore": [
                "node_modules"
              ]
            }
            """))
    else:
        return True


def ensure_node_modules(ctx):
    """Has node init been called? (if not call it).
    """
    node_modules = os.path.join(ctx.pkg.root, 'node_modules')
    if not os.path.exists(node_modules):
        with cd(ctx.pkg.root):
            ctx.run("npm install --no-color")
    else:
        return True


# def ensure_babel(ctx):
#     if 'babel' not in runners.run("npm ls -g --depth=0 babel --no-color"):
#         print("didn't find babel, installing it..")
#         with cd(ctx.pkg.root):
#             ctx.run("npm install -g babel")
#     else:
#         return True


# def ensure_browserify(ctx):
#     if 'browserify' not in runners.run("npm ls -g --depth=0 browserify --no-color"):
#         print("didn't find browserify, installing it..")
#         with cd(ctx.pkg.root):
#             ctx.run("npm install -g browserify")
#     else:
#         return True


def ensure_es2015(ctx):
    if 'babel-preset-es2015' not in runners.run("npm ls --depth=0 babel-preset-es2015 --no-color"):
        print("didn't find babel-preset-es2015, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-es2015 --save-dev")
    else:
        return True


def ensure_preset_es2016(ctx):
    if 'babel-preset-es2015' not in runners.run("npm ls --depth=0 babel-preset-es2016 --no-color"):
        print("didn't find babel-preset-es2016, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-es2016 --save-dev")
    else:
        return True


def ensure_preset_es2017(ctx):
    if 'babel-preset-es2017' not in runners.run("npm ls --depth=0 babel-preset-es2017 --no-color"):
        print("didn't find babel-preset-es2017, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-es2017 --save-dev")
    else:
        return True


def ensure_preset_latest(ctx):
    if 'babel-preset-env' not in runners.run("npm ls --depth=0 babel-preset-env --no-color"):
        print("didn't find babel-preset-env, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-env --save-dev")
    else:
        return True


def ensure_preset_babili(ctx):
    if 'babel-preset-babili' not in runners.run("npm ls --depth=0 babel-preset-babili --no-color"):
        print("didn't find babel-preset-babili, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-babili --save-dev")
    else:
        return True


def ensure_babelify(ctx):
    if 'babelify' not in runners.run("npm ls --depth=0 babelify --no-color"):
        print("didn't find babelify, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install --save-dev babelify --no-color", echo=False, encoding='utf-8')
    else:
        return True


def ensure_babel_minify(ctx):
    nodepkgs = runners.run("npm ls --depth=0 babelify --no-color")
    if 'babel-minify' not in nodepkgs and 'minify' not in nodepkgs:
        print("didn't find babelify, installing it..")
        with cd(ctx.pkg.root):
            ctx.run("npm install --save-dev babelify --no-color", echo=False, encoding='utf-8')
    else:
        return True


# FIXME: cannot use @requires this way since it causes download/install of
# requirements when this file is imported (not when the function is used!)

# @requires('nodejs', 'npm', 'babel')
# @task
# def babel(ctx, source, dest=None, source_maps=True, force=False):
#     """
#     --source-maps --out-file $ProjectFileDir$/$ProjectName$/static/$ProjectName$/$FileNameWithoutExtension$.js $FilePath$
#     """
#     source = Path(source.format(pkg=ctx.pkg))
#     if dest is None:
#         dest = ctx.pkg.django_static / ctx.pkg.name / 'js'
#         dest.makedirs()
#     else:
#         dest = Path(dest.format(pkg=ctx.pkg))
#     if dest.isdir():
#         dest = dest / switch_extension(source.basename(), '.js')

#     if not force and dest_is_newer_than_source(source, dest):
#         print('babel:', dest, 'is up-to-date.')
#         return dest

#     ensure_package_json(ctx)
#     ensure_node_modules(ctx)
#     # ensure_babel(ctx)
#     # ensure_es2015(ctx)
#     ensure_preset_latest(ctx)
#     ensure_babelrc(ctx)

#     options = ""
#     if source_maps:
#         options += " --source-maps"

#     ctx.run("babel {options} --out-file {dest} {source}".format(**locals()))
#     return dest


def version_js(ctx, fname, kind='pkg', force=False):
    """Add version number to a .js file.
    """
    dst = copy_to_version(
        ctx,
        fname,
        kind=kind,
        force=force
    )
    return dst


@requires('nodejs', 'npm', 'browserify')
@task
def browserify(ctx,
               source, dest,
               babelify=False,
               require=(),
               external=(),
               entry=None):
    """
    Run ``browserify``

    Args:
        ctx (pyinvoke.Context):  context
        source (str):            root source file
        dest (str):              path/name of assembled file
        babelify (Bool):         use babel transform
        require (iterable):      A module name or file to bundle.require()
                                 Optionally use a colon separator to set the target.
        external:                Reference a file from another bundle. Files can be globs.
        entry:

    Returns:
        None

    """
    print('ensure package.json:', ensure_package_json(ctx))
    print('ensure node_modules:', ensure_node_modules(ctx))
    # print('ensure browserify:', ensure_browserify(ctx))

    # options = "--debug"  # source maps
    options = ""  # no source maps
    if babelify:
        print('ensure babelify:', ensure_babelify(ctx))
        print('ensure preset latest:', ensure_preset_latest(ctx))
        options += ' -t babelify'
        options += ' --presets env'
    for r in require:
        options += ' -r "%s"' % r
    for e in external:
        options += ' -x "%s"' % e
    if entry:
        options += ' -e "%s"' % entry
    cmd = "browserify {source} -o {dest} {options}".format(**locals())
    ctx.run(cmd)
    with open(dest, 'rb') as fp:
        txt = fp.read()
    if '\r\n' in txt:
        with open(dest, 'wb') as fp:
            fp.write(txt.replace('\r\n', '\n'))
    return dest


babilicmd = Command('babili', '{src} {opts} -o {dst}',
                    requirements=('nodejs', 'npm', 'babili'))


@requires('nodejs', 'npm', 'babili')
@task
def babili(ctx, src, dst):
    babilicmd(
        ctx,
        src=src,
        dst=dst,
    )
    return dst


# babel-minify is linked to minify
babel_minifycmd = Command('babel-minify', '{src} {opts} -o {dst}',
                          requirements=('nodejs', 'npm', 'babel-minify'))


@requires('nodejs', 'npm', 'babel-minify')
@task
def babel_minify(ctx, src, dst):
    """
    dkjs/node_modules/.bin> babel-minify --help

      Usage: minify index.js [options]

      IO Options:
        --out-file, -o          Output to a specific file
        --out-dir, -d           Output to a specific directory

      Transform Options:
        --mangle                Context and scope aware variable renaming
        --simplify              Simplifies code for minification by reducing statements into
                                expressions
        --booleans              Transform boolean literals into !0 for true and !1 for false
        --builtIns              Minify standard built-in objects
        --consecutiveAdds       Inlines consecutive property assignments, array pushes, etc.
        --deadcode              Inlines bindings and tries to evaluate expressions.
        --evaluate              Tries to evaluate expressions and inline the result. Deals
                                with numbers and strings
        --flipComparisons       Optimize code for repetition-based compression algorithms
                                such as gzip.
        --infinity              Minify Infinity to 1/0
        --memberExpressions     Convert valid member expression property literals into plain
                                identifiers
        --mergeVars             Merge sibling variables into single variable declaration
        --numericLiterals       Shortening of numeric literals via scientific notation
        --propertyLiterals      Transform valid identifier property key literals into identifiers
        --regexpConstructors    Change RegExp constructors into literals
        --removeConsole         Removes all console.* calls
        --removeDebugger        Removes all debugger statements
        --removeUndefined       Removes rval's for variable assignments, return arguments from
                                functions that evaluate to undefined
        --replace               Replaces matching nodes in the tree with a given replacement node
        --simplifyComparisons   Convert === and !== to == and != if their types are inferred
                                to be the same
        --typeConstructors      Minify constructors to equivalent version
        --undefinedToVoid       Transforms undefined into void 0

      Other Options:
        --keepFnName            Preserve Function Name (useful for code depending on fn.name)
        --keepClassName         Preserve Class Name (useful for code depending on c.name)
        --keepFnArgs            Don't remove unused fn arguments (useful for code depending on fn.length)
        --tdz                   Detect usages of variables in the Temporal Dead Zone

      Nested Options:
        To use nested options (plugin specfic options) simply use the pattern
        --pluginName.featureName.

        For example,
        minify index.js --mangle.keepClassName --deadcode.keepFnArgs --outFile index.min.js
    """
    # if os.path.exists(dst):
    #     os.unlink(dst)

    babel_minifycmd(
        ctx,
        src=src,
        dst=dst,
        keepFnName=True,
        keepClassName=True,
        mangle=False,
        simplify=False,
        builtIns=True,
        deadcode=False,
        evaluate=False
    )
    return dst


# @task(default=True)
# def buildjs(ctx, src, dst, force=False, **kw):
#     uglify = kw.pop('uglify', False)
#     if kw.pop('browserify', False):
#         dst = browserify(ctx, src, dst,
#                          babelify=kw.pop('babelify', src.endswith('.jsx')), **kw)
#     else:
#         dst = babel(ctx, src, dst, force=force)

#     if uglify:
#         finaldst = switch_extension(dst, '.min.js')
#         dst = uglifyjs(ctx, dst, finaldst)
#         if force:
#             dst = copy_to_version(ctx, dst, force=force)

#     return dst


uglifycmd = Command('uglifyjs', '{src} {opts} -o {dst}',
                    requirements=('nodejs', 'npm', 'uglify'))


@requires('nodejs', 'npm', 'uglify')
@task
def uglifyjs(ctx,
             src, dst,
             compress=True, mangle=True):
    uglifycmd(
        ctx,
        src=src,
        dst=dst,
        compress=compress,
        mangle=mangle
    )
    return dst


@task(default=True)
def buildjs(ctx, src, dst, force=False, **kw):
    uglify = kw.pop('uglify', False)
    if kw.pop('browserify', False):
        dst = browserify(ctx, src, dst,
                         babelify=kw.pop('babelify', src.endswith('.jsx')), **kw)
    else:
        # dst = babel(ctx, src, dst, force=force)
        pass

    if uglify:
        finaldst = switch_extension(dst, '.min.js')
        dst = uglifyjs(ctx, dst, finaldst)
        if force:
            dst = copy_to_version(ctx, dst, force=force)

    return dst


ns = Collection(browserify, uglifyjs)
ns.configure({
    'static': 'static/{pkg.name}'
})
