from setuptools import setup, find_packages

from codecs import open
from os import path

from tpmontrouge import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tpmontrouge',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='Package Python pour les TPs de Montrouge',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/PrepaAgregMontrouge/interfacage',

    # Author details
    author='Pierre Cladé',
    author_email='pierre.clade@lkb.upmc.fr',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',

    ],

    # What does your project relate to?
    keywords='scope bode diagramm instrument',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
#    install_requires=['cached_property', 'numpy', 'scipy'],

#    # List additional groups of dependencies here (e.g. development
#    # dependencies). You can install these using the following syntax,
#    # for example:
#    # $ pip install -e .[dev,test]
#    extras_require={
#        'dev': ['check-manifest'],
#        'test': ['coverage'],
#    },

#    # If there are data files included in your packages that need to be
#    # installed, specify them here.  If using Python 2.6 or less, then these
#    # have to be included in MANIFEST.in as well.
#    package_data={
#        'sample': ['package_data.dat'],
#    },

#    # Although 'package_data' is the preferred approach, in some case you may
#    # need to place data files outside of your packages. See:
#    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
#    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
#    data_files=[('my_data', ['data/data_file'])],

#    # To provide executable scripts, use entry points in preference to the
#    # "scripts" keyword. Entry points provide cross-platform support and allow
#    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'tpmontrouge-bode=tpmontrouge.interface.bode_plot.main:main',
            'tpmontrouge-scope=tpmontrouge.interface.scope.main:main',
            'tpmontrouge-full-gui=tpmontrouge.interface.main:main',
            'tpmontrouge=tpmontrouge.main:main',
        ],
    },
)
