import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pysophia2",
    version="0.1.3",
    description="Python library for news discourse analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TeamSophia2/pySophia2",
    author="Team Sophia2",
    author_email="mvernier@inf.uach.cl",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["pysophia2"],
    install_requires=["pandas", "mariadb", "elasticsearch>=7.16.3", "spacy", "matplotlib", "numpy"],

)