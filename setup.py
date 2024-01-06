import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt")) as f:
    install_requires = f.readlines()

setup(
    name="secretSanta",
    version="0.0.1",
    description="Organize Secret Santa by email",
    url="https://github.com/malihass/SecretSanta",
    license="",
    package_dir={"secretSanta": "secretSanta"},
    classifiers=[
        "Intended Audience :: General",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=install_requires,
)
