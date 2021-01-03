import setuptools

name = "yamlval"
__version__ = "1.0.0"

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=name,
    version=__version__,
    author="Michael DiGregorio",
    author_email="mjm.digregorio@gmail.com",
    description="A YAML type validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mycicle/yamlval",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml >= 5.3.1', 
        'loguru >= 0.5.3'
    ],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: MIT License",
        "Operating System :: OS Independent"
    ),
)