#!/bin/python3
import fileinput
import os
import sys

import setuptools

from dynamicforms import __version__


def write_ver_to_init(file_name: str, version: str, search: str, replacement: str):
    replacement = replacement % version
    filename = file_name
    for line in fileinput.input([filename], inplace=True):
        if line.strip().startswith(search):
            line = replacement
        sys.stdout.write(line)


def get_version(version_arg):
    from versio.version import Version
    from versio.version_scheme import Simple3VersionScheme

    try:
        if version_arg == "publish":
            print("Missing version argument.")
            sys.exit(1)
        Version(version_arg, scheme=Simple3VersionScheme)
    except Exception:
        print("Invalid version format. Should be x.y.z (all numbers)")
        sys.exit(1)
    return version_arg


with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

version_str = __version__

if sys.argv[1] == "publish":
    version_str = get_version(sys.argv[-1])

    if os.system("python -m wheel version"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("python -m twine --version"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    if os.system("tox -e check") or os.system("npm run test"):
        sys.exit()

    write_ver_to_init("dynamicforms/__init__.py", version_str, "__version__", "__version__ = '%s'\n")
    write_ver_to_init("vue/dynamicforms/package.json", version_str, '"version": ', '  "version": "%s",\n')

    os.system("npm run build")
    os.system("cd vue/dynamicforms && npm publish && cd ../..")

    os.system("python setup.py sdist bdist_wheel")
    # if you don't like to enter username / pass for pypi every time, run this command:
    #  keyring set https://upload.pypi.org/legacy/ username  (it will ask for password)
    os.system("twine upload dist/*")
    os.system("rm -rf build && rm -rf dist && rm -rf DynamicForms.egg-info")
    os.system("git checkout dynamicforms/__init__.py")
    os.system("git checkout vue/dynamicforms/package.json")
    os.system("git tag -a %s -m 'version %s'" % (version_str, version_str))
    os.system("git push --tags")
    sys.exit()

setuptools.setup(
    name="DynamicForms",
    version=version_str,
    author="Jure Erznožnik",
    author_email="jure@velis.si",
    description="DynamicForms performs all the visualisation & data entry of your DRF Serializers & ViewSets and adds "
    "some candy of its own: It is a django library that gives you the power of dynamically-shown form "
    "fields, auto-filled default values, dynamic record loading and similar candy with little effort. "
    "To put it differently: once defined, a particular ViewSet / Serializer can be rendered in multiple "
    "ways allowing you to perform viewing and authoring operations on the data in question.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/velis74/DynamicForms",
    packages=setuptools.find_packages(include=("dynamicforms", "dynamicforms_legacy")),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)
