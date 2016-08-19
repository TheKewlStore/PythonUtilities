import argparse
import pexpect
import os

from setuptools import setup, find_packages

VERSION = "1.0.14"


def create_packages():
    setup(
        name='python_utilities',
        version=VERSION,
        packages=(find_packages()),
        install_requires=['colorlog', ],
        url = 'https://github.com/TheKewlStore/PythonUtilities',
        license = '',
        author = 'Ian Davis',
        author_email = 'thekewlstore@gmail.com',
        description = "A set of simple utility APIs for higher-level python functions.",
        script_name = 'setup.py',
        script_args = ['sdist', 'bdist_wheel'],
    )


def upload_packages():
    upload_process = pexpect.spawn('twine upload dist/*')
    upload_process.expect(['username:'])
    upload_process.sendline('TheKewlStore')
    upload_process.expect(['password:'])
    upload_process.sendline('Kewl1store')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build script for PythonUtilities package.')
    parser.add_argument('release_type', help='The type of version build', choices=['patch', 'minor', 'major'])
    args = parser.parse_args()
    os.system('bumpversion {0}'.format(args.release_type))
    create_packages()
    upload_packages()

