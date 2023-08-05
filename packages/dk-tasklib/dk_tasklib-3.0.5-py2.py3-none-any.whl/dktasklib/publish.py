from dktasklib.executables import requires
from dktasklib.wintask import task
from . import Package


@requires('wheel', 'twine')
@task(
    default=True,
    help={
        'force': 'sets all other options to True',
        'clean': 'remove the build/ and dist/ directory before starting',
        'docs': 'build and upload docs to PyPi',
        'wheel': 'build wheel (in addition to sdist)',
        'sign': 'sign the wheel using weel sign pkgname',
        'upload': 'upload to PyPI after building'
    }
)
def publish(ctx, force=False, clean=True, wheel=True, sign=True, docs=False, upload=False):
    """Publish to PyPi
    """
    pkg = Package()
    if force:  # pragma: nocover
        clean = True
        wheel = True
        docs = True
        upload = True
        sign = True     # noqa

    if not wheel:
        sign = False    # noqa

    with pkg.root.cd():
        if clean:
            ctx.run("rm -rf dist")
            ctx.run("rm -rf build/lib")
            ctx.run("rm -rf build/bdist.win32")

        targets = 'sdist'
        if wheel:
            targets += ' bdist_wheel'

        ctx.run("python setup.py " + targets)

        # if sign:
        #     for fname in glob.glob('dist/*.whl'):
        #         ctx.run('wheel sign ' + fname)

        if docs:
            ctx.run("python setup.py build_sphinx")

        if upload:
            ctx.run("twine upload dist/*")
        else:
            print("Not uploading (use --upload flag to upload).")

        # if docs and upload:
        #     # we can't upload docs to pypi anymore.. (or can we..?)
        #     ctx.run("python setup.py upload_docs")
