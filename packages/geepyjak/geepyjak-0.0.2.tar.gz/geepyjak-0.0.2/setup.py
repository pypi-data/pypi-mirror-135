from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'earth engine function imports'
LONG_DESCRIPTION = 'This package is written to import various earth engine function easily'

setup(
    name="geepyjak",
    version=VERSION,
    author="Antony Kishoare J",
    author_email="<a060697.ak@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['earthengine-api', 'geemap'],

    keywords=['ee', 'geepyjak'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)