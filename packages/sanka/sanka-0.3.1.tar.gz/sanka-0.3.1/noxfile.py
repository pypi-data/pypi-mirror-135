import nox
import re

from distutils.util import strtobool
from os import environ as envvar
from subprocess import check_output
from subprocess import Popen
from subprocess import PIPE
from typing import List


OFFICIAL = strtobool(envvar.get('OFFICIAL', 'False'))
PROJECT_NAME = 'sanka'
VENV = f'{PROJECT_NAME}-venv'
TESTDIR = '.'
TESTNAME = envvar.get('TESTNAME', '')
USEVENV = envvar.get('USEVENV', False)
EXAMPLE = envvar.get('EXAMPLE', 'actionpack')

external = False if USEVENV else True
unofficial_semver = r'^([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?(.+)$'
official_semver = r'^([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$'
supported_python_versions = [
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
]

nox.options.default_venv_backend = 'none' if not USEVENV else USEVENV

def session_name(suffix: str):
    return f'{VENV}-{suffix}' if USEVENV else suffix


def semver(version: str):
    _semver = re.search(official_semver, version) or re.search(unofficial_semver, version)
    if _semver:
        return [val for val in _semver.groups() if val]


def is_official(semver: List[str]):
    """
    TODO (withtwoemms) -- create SemVer type to replace List[str]
    """
    if len(semver) > 3:
        return False
    else:
        return True


def latest_version(official: bool = False):
    output = check_output('git for-each-ref --sort=creatordate --format %(refname) refs/tags'.split())
    all_versions = (
        version.lstrip('refs/tags/')
        for version in reversed(output.decode().strip('\n').split('\n'))
    )

    if not official:
        return next(all_versions)

    for version in all_versions:
        if official and is_official(semver(version)):
            return version


def image_name(official: bool = False):
    return f'{PROJECT_NAME}:{latest_version(official=official)}'


@nox.session(name=session_name('version'), python=supported_python_versions)
def version(session):
    print(latest_version(official=OFFICIAL))


@nox.session(name=session_name('image'), python=supported_python_versions)
def image(session):
    command = f'docker build -t {image_name(official=OFFICIAL)} -f examples/{EXAMPLE}/Dockerfile --build-arg EXAMPLE={EXAMPLE} .'
    session.run(*command.split(' '))


@nox.session(name=session_name('install'), python=supported_python_versions)
def install(session):
    session.run(
        'python', '-m',
        'pip', '--disable-pip-version-check', 'install', '.',
        external=external
    )
    session.run(
        'python', '-m',
        'pip', '--disable-pip-version-check', 'install', '-r', 'requirements.txt',
        external=external
    )


@nox.session(name=session_name('test'), python=supported_python_versions)
def test(session):
    if USEVENV:
        install(session)

    session.run(
        'python', '-m',
        'coverage', 'run', '--branch',
        '--omit', '.nox/*,noxfile.py,setup.py,test*',
        '--source', '.',
        '-m', 'unittest', TESTNAME if TESTNAME else f'discover',
        external=external
    )
    session.run('coverage', 'report', '-m', external=external)
    session.run('coverage', 'xml', external=external)


@nox.session(name=session_name('build'), python=supported_python_versions)
def build(session):
    session.run('python', 'setup.py', 'sdist')

