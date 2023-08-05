This document discusses setting up local development for this project on your own personal development machine. 

## Install Dependencies 

It is wise to do development in an virtual environment.

    python3 -m venv venv
    source venv/bin/activate

Now dependencies can be installed!
For development, you SHOULD to use the dependencies that are specified in `requirements.txt`:

    pip install -r requirements.txt

## Running from Source

To run this project from source code, we use the `--editable` flag with `pip install` against the locally downloaded repository.

    # run from the directory where setup.py lives
    pip install --editable .

This will install this project into your site-packages.
Using this feature, any changes you make in the locally downloaded repo will be reflected when testing the code!

## Dependency Management

We use `requirements.txt` to define all dependencies for development, while `setup.py` holds a *looser* list of package that are installed when the package is installed via pip.
This follows [general Python practices, (discussed on python.org)](https://packaging.python.org/discussions/install-requires-vs-requirements/#install-requires)

### Development Dependencies: `requirements.txt`

`requirements.txt` holds all of the development dependencies for this project.

If you make changes to dependencies, be sure to update requirements.txt.
The following command will update requirements.txt (and will correctly omit 'editable' packages).

    pip freeze | grep -i ^-e > requirements.txt

### Production Dependencies: `setup.py`

In `setup.py`, there is the **minimum** List of packages required for installation: `install_requires`.
This list should follow best practices, I.e.,

1. do **NOT** pin specific versions, and 
2. do **NOT** specify sub-dependencies.

## Automated Testing

pytest is used for unit testing, integration testing, and end-to-end testing of this solution.

Run the `pytest` CLI tool from the local directory to run all of the tests!

    pytest 