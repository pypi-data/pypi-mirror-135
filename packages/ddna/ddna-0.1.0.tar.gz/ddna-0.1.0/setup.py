# pylint: skip-file
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []

setup(
    name="ddna",
    version="0.1.0",
    author="Aayush Pokharel",
    author_email="aayushpokharel36@gmail.com",
    description="Encode and decode strings to DNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aayush9029/DDNA",
    py_modules=["ddna"],
    packages=find_packages(),
    install_requires=requirements,
    requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
