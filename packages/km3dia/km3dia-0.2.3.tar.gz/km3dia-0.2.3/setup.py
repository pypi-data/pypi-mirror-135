#!/usr/bin/env python
# Filename: setup.py
"""
The km3dia setup script.

"""
from setuptools import setup
import os


def read_requirements(kind):
    """Return a list of stripped lines from a file"""
    with open(os.path.join("requirements", kind + ".txt")) as fobj:
        return [l.strip() for l in fobj.readlines()]


try:
    with open("README.rst") as fh:
        long_description = fh.read()
except UnicodeDecodeError:
    long_description = "Python module providing access to DIA DB information."

setup(
    name="km3dia",
    url="https://git.km3net.de/km3py/km3dia",
    description="Python module providing access to DIA DB information.",
    long_description=long_description,
    author="Valentin Pestel",
    author_email="vpestel@km3net.de",
    packages=["km3dia"],
    include_package_data=True,
    platforms="any",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    python_requires=">=3.6",
    install_requires=read_requirements("install"),
    extras_require={kind: read_requirements(kind) for kind in ["dev"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
    ],
)
