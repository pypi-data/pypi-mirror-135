from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Incubeta first Python package'
LONG_DESCRIPTION = 'Incubeta first Python package for preprocessing data'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="tool_prep_data",
    version=VERSION,
    author="Chigozie Boniface",
    author_email="chigface@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['scikit-learn', 'pandas', 'numpy'], # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)