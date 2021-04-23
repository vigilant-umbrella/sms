# Contributing Guide

## Development procedure-

### Before making changes:

- Create new git branch

  `git switch -c <branch-name>`

- Start a virtual environment

  `pipenv shell`

- Install updated python packages

  `pipenv install --dev`

### Before putting changes in production (pushing to repo):

- Run tests

  `pytest tests`

- Lock package dependencies

  `pipenv lock`

### To install a new Python package:

- Installing package necessary for application

  `pipenv install <package-name>`

- Installing package needed only for development

  `pipenv install <package-name> --dev`

### To run tests

- Run tests using pytest

  `pytest tests`

## Compilation Steps for Linux

### To compile the file:

```
pyinstaller --onefile --name sms --clean --distpath . --log-level ERROR system_monitoring_system/__main__.py
```

### To run the compiled file from anywhere in the system:

```
sudo cp sms /usr/local/bin
```

### Call the application using

```
sms <ARGS>

```

## How to use the core.Get().process() method?

### Example code

```
import core

g = core.Get()

for process in ﻿g.process():
    print(process)

```

The above code will print all process dictionaries.

### Example code to print at most 50 processes.

```
import core

g = core.Get()
processes = g.process()

num = 0
while num < 50:
    try:
        process = next(processes)
    except StopIteration:
        break
    print(process)
    num += 1

```
