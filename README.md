# SecretSanta [![secret-santa-email-CI](https://github.com/malihass/secretSanta/actions/workflows/ci.yml/badge.svg)](https://github.com/malihass/secretSanta/actions/workflows/ci.yml) [![secret-santa-email-pyversion](https://img.shields.io/pypi/pyversions/secret-santa-email.svg)](https://pypi.org/project/secret-santa-email/)  [![secret-santa-email-pypi](https://badge.fury.io/py/secret-santa-email.svg)](https://badge.fury.io/py/secret-santa-email) 

Organize Secret Santa by email

Some key features
- Email addresses are not shared to anyone
- The host cannot see the result of the match-making
  - The send email are purged after match making
  - The results of the match making are logged (if needed) to pickle file
- One can specify what match pairs to avoid (avoids having the same match pairs a few years in a row)
- Partners receive a notification about match making pairs of interest to them so they can sync up their gift

## Installation for developers

```bash
conda create --name secretSanta python=3.10
conda activate secretSanta
git clone https://github.com/malihass/secretSanta.git
cd secretSanta
pip install -e .
```

## Installation for users

```bash
conda create --name secretSanta python=3.10
conda activate secretSanta
pip install secret-santa-email
```

### Quick start

1. `cd applications; python main.py`: outputs the match making result for a sample party

2. Check the test suites in `tests`

## Formatting [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Code formatting and import sorting are done automatically with `black` and `isort`. 

Fix imports and format : `pip install black isort; bash fixFormat.sh`

Spelling is checked but not automatically fixed using `codespell`

## TODO list
- Add a web interface

## Contact

Malik Hassanaly: (malik.hassanaly!at!gmail!com)

Senna Hassanaly: (senna.hassanaly!at!departmentofdogs!com)

