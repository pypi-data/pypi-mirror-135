from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="tei-validator",
    description="TEI XML validation package",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    version=VERSION,
    include_package_data=True,
    py_modules=["tei_validator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lxml~=4.6"
    ],
    extras_require={
        "test": ["pytest~=6.2"],
        "dist": ["build~=0.7", "twine~=3.6"],
    },
    entry_points={
        "console_scripts": ["tei-validator = tei_validator:cli"]
    },
    python_requires=">=3.7",
)
