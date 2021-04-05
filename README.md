# System Monitoring System

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
