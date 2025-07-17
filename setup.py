from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="enview",
    version="1.0.4",
    author="Chivier Humber",
    install_requires=[
        "click>=8.0.3,<9.0.0",
        "fuzzywuzzy==0.18.0",
        "jellyfish>=0.9.0,<2.0.0",
        "mypy-extensions>=0.4.3,<2.0.0",
        "pathspec>=0.9.0,<1.0.0",
        "platformdirs>=2.4.1,<5.0.0",
        "prettytable>=3.0.0,<4.0.0",
        "prompt-toolkit>=3.0.26,<4.0.0",
        "Pygments>=2.11.2,<3.0.0",
        "pyparsing>=3.0.7,<4.0.0",
        "python-nubia==0.2b5",
        "readchar>=3.0.5,<5.0.0",
        "termcolor>=1.1.0,<4.0.0",
        "tomli>=1.2.3,<3.0.0",
        "typing-inspect>=0.7.1,<1.0.0",
        "typing_extensions>=4.0.1,<5.0.0",
        "wcwidth>=0.2.5,<1.0.0",
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
