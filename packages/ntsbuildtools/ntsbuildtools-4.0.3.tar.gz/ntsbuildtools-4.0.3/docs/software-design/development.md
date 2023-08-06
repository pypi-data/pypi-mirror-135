This document discusses setting up local development for this project on your own personal Linux box. 

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

    pytest --doctest-modules

### Doctests

In addition to general pytest test cases, we also have some [doctest](https://docs.python.org/3/library/doctest.html) test cases.
pytest will execute those test cases with an additional argument, `--doctest-modules`. 

> Always run `pytest` with the `--doctest-modules` argument to ensure that our doctest test cases are up to date!

## End-to-end (e2e) Test Cases

End-to-end (e2e) automated testing is driven via pytest, just like all the other test cases.
However, we have some additional tools and protocols for managing e2e test cases. 

### Handling e2e Secret Values

E2e test cases often depend on some secret value to enable authenticating against some real/product endpoint, think 'password' or 'api token.'
Those should be pulled from environment variables and **NEVER SAVED IN CODE**.

We use pytest fixtures to expose any secret values needed by test cases.
The pytest fixtures simply needs to gather and return the environment variable.
An example is below:

    import os
    import pytest

    # Setup a fixture to retrieve a password from an environment variable.
    @pytest.fixture
    def password():
        return os.environ.get('BITBUCKET_PASSWORD', '')  # Provide a default, to enable vcrpy cassette replays
    
    # Run a test case with that password
    def test_e2e_bitbucket(password):
        make_some_bitbucket_request(password)

> NOTE: When replaying an e2e test case via a vcrpy cassette, environment variables can be omitted!

### vcrpy

E2e testing is recorded and replayed with [vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html).

vcrpy has many benefits: 

* E2e test cases run VERY QUICKLY.
* E2e test cases can be run as regression tests without setting up any 'e2e Secret Values' (in local 
development or continuous integration pipelines).

There is one big drawback of vcrpy:

* Special sanitization code is required to ensure that the recorded HTTP request/response does not contain any secret values!

### vcrpy -- Sanitizing Cassettes

We sanitize the recorded HTTP requests using some logic in the `tests/conftest.py` file.
Specifically, I have set up the following filters at the time of writing:

* Filter out 'Basic Authorization' HTTP Headers.
    * See [Filtering Data from the Request](https://vcrpy.readthedocs.io/en/latest/advanced.html#filter-sensitive-data-from-the-request)
* Replace 'webhook' request URIs with a dummy URI.
    * Microsoft Teams puts a Webhook secret directly in the URI!
    * See [Custom Request Filtering](https://vcrpy.readthedocs.io/en/latest/advanced.html#custom-request-filtering)

### vcrpy -- How to Re-recorded a Test Case?

When you have some e2e test cases that have been recorded as cassettes, you may wonder "what is the best way to actually re-run the test case against the *real* production endpoint?"

* Answer: **Delete the associated `cassettes/*.yaml` file.**

Our scheme in this project is to only maintain ONE recording for each test case.
So, the best way to re-record a test case e2e is to simply delete the associated cassette (HTTP recording) YAML file, which forces vcrpy to actually run the test case e2e, and will generate a new recording!

> There is no need to ever mess with the 'vcr-record-mode' using this scheme!
