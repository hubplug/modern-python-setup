import tempfile

import nox


# nox session for automated tests
@nox.session(python=["3.8", "3.7"])
def tests(session):
    # no end-to-end tests for default automated unit testing
    # e.g. nox -r
    # use -m e2e to run end-to-end tests
    # e.g. nox -rs tests-3.8 -- -m e2e
    # (run end-to-end tests inside the testing environment for Python 3.8)
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


# nox session for linting
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7"])
def lint(session):
    args = session.posargs or locations
    # session.install() installs package(s) into virtual env via pip
    # session.install("flake8")
    # add flake8-black to generate black warning (without modifying file)
    # session.install("flake8", "flake8-black")
    # add flake8-import-order to check import order
    # alternative to flake8-import-order: flake8-isort
    #   also: asottile/reorder-python-imports and sqlalchemyorg/zimports
    # session.install("flake8", "flake8-black", "flake8-import-order")
    # add flake8-bugbear to check additional bugs or design problems
    # session.install("flake8", "flake8-black", "flake8-bugbear", "flake8-import-order")
    # add flake8-bandit to check security issues
    # alternative to flake8-bandit: python-afl
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


# by default, Nox runs all sessions defined in noxfile.py.
# use the --session (-s) option to restrict it to a specific session.
# e.g. nox -rs tests (only run tests)
# e.g. nox -rs lint (only run lint)


# nox session for code formatting (black)
@nox.session(python="3.8")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


# nox session for dependency (library/package) security check (safety)
# uses the poetry export command to convert poetry’s lock file to a requirements file
# the standard tempfile module is used to create a temporary file for the requirements
@nox.session(python="3.8")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


# define sessions run by default, excluding "black"
# i.e. do not run black and modify file(s) all the time
nox.options.sessions = "lint", "safety", "tests"
