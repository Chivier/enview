import pathlib
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="enview",
    version="1.0.1",
    author="Chivier Humber",
    install_requires=[
        'click==8.0.3',
        'edit==0.0.4',
        'fuzzywuzzy==0.18.0',
        'jellyfish==0.9.0',
        'mypy-extensions==0.4.3',
        'pathspec==0.9.0',
        'platformdirs==2.4.1',
        'prettytable==3.0.0',
        'prompt-toolkit==3.0.26',
        'Pygments==2.11.2',
        'pyparsing==3.0.7',
        'pyperclip==1.8.2',
        'python-nubia==0.2b5',
        'readchar==3.0.5',
        'termcolor==1.1.0',
        'tomli==1.2.3',
        'typing-inspect==0.7.1',
        'typing_extensions==4.0.1',
        'wcwidth==0.2.5'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chivier/enview",
    author_email="chivier.humber@outlook.com",
    entry_points={
        "console_scripts": ["enview=enview.enview:main"],
    },
    license="Apache-2.0 License",
    keywords="translator",
    packages=find_packages(),
)
