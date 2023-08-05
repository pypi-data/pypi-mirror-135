from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This is dictionary translation library there are three input parameter where we have to cahnge values in the dictionary'


# Setting up
setup(
    name="datatranslation",
    version=VERSION,
    author="sairam",
    author_email="saira160305@gmail.com",
    description='This is dictionary translation library there are three input parameter where we have to cahnge values in the dictionary',
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)