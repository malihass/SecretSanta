import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "secretSanta", "requirements.txt")) as f:
    install_requires = f.readlines()

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open(
    os.path.join(here, "secretSanta", "version.py"), encoding="utf-8"
) as f:
    version = f.read()
version = version.split("=")[-1].strip().strip('"').strip("'")

setup(
    name="secret-santa-email",
    version=version,
    description="SecretSanta: a toolbox for organizing secret Santa by email",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/malihass/SecretSanta",
    author="Malik Hassanaly",
    license="BSD 3-Clause",
    package_dir={"secretSanta": "secretSanta"},
    package_data={"": ["requirements.txt", "guests.json"]},
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
)
