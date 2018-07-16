#!/usr/bin/python
#  Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os


try:
    from pip import download
except ImportError:
    # Pip 10 support
    from pip._internal import download

try:
    from pip import req
except ImportError:
    # Pip 10 support
    from pip._internal import req

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def get_requirements(reqfile):
    file_path = os.path.join(HERE, reqfile)
    deps = set()
    for dep in req.parse_requirements(file_path, session=download.PipSession()):
        try:
            # Pip 8.1.2 Compatible
            specs = ','.join(''.join(str(spec)) for spec in dep.req.specifier)
        except AttributeError:
            # Pip 1.5.4 Compatible
            specs = ','.join(''.join(spec) for spec in dep.req.specs)
        requirement = '{name}{extras}{specs}'.format(
            name=dep.name,
            extras=(
                '[{extras}]'.format(extras=','.join(dep.extras))
                if dep.extras else ''
            ),
            specs=specs,
        )

        deps.add(requirement)
    return list(deps)

setup(
    name='geo_api',
    version='versiontools:geo_api:',

    description='My geo api endpoint',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ssoto/geo_api',

    # Author details
    author='Sergio Soto',
    author_email='sergio.soto.nunez@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='sample geo api flask',

    packages=find_packages(),

    install_requires=get_requirements('requirements/requirements.txt'),
    tests_require=get_requirements('requirements/test-requirements.txt'),
    setup_requires=('versiontools'),

    include_package_data=True,

)