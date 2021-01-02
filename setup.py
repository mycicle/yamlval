import setuptools
from yamlval.__init__ import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="yamlval",
    version=__version__,
    author="Michael DiGregorio",
    author_email="mjm.digregorio@gmail.com",
    description="A YAML type validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mycicle/yamlval",
    packages=setuptools.find_packages(),
    install_requires=["pyyaml", "loguru"],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: MIT License",
        "Operating System :: OS Independent"
    ),
)