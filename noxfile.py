import tempfile

import nox


# instead of simply using "poetry install" (like for pytest), which installs a whole
# bunch of dependencies required for testing but not necessarily for linting &
# formatting, use poetry to generate "dev only" "requirements.txt" and pass it to
# pip to install only dev dependencies and with correct version (pinning)
def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        # session.install() installs package(s) into virtual env via pip
        # --constraint file specifies which version(s) to install
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


# nox session for automated tests
@nox.session(python=["3.8", "3.7"])
def tests(session):
    # no end-to-end tests for default automated unit testing
    # e.g. nox -r
    # use -m e2e to run end-to-end tests
    # e.g. nox -rs tests-3.8 -- -m e2e
    # (run end-to-end tests inside the testing environment for Python 3.8)
    args = session.posargs or ["--cov", "-m", "not e2e"]
    # session.run("poetry", "install", external=True)
    # instead of poetry install everything, which includes all dev dependencies,
    # use poetry install with --no-dev, and then install dev dependencies
    # only necessary for testing, using install_with_constraints()
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


# define package name
package = "modern_python_setup"


# nox session to do runtime type checking (typeguard)
@nox.session(python=["3.8", "3.7"])
def typeguard(session):
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    # run typeguard with pytest plugin by passing "--typeguard-packages=..."
    session.run("pytest", f"--typeguard-packages={package}", *args)


# locations for linting & formatting
locations = "src", "tests", "noxfile.py"


# nox session for linting
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
    # session.install(
    #     "flake8",
    #     "flake8-bandit",
    #     "flake8-black",
    #     "flake8-bugbear",
    #     "flake8-import-order",
    # )
    # change do call install_with_constraints() instead of session.install()
    install_with_constraints(
        session,
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
    # session.install("black")
    # change do call install_with_constraints() instead of session.install()
    install_with_constraints(session, "black")
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
        # session.install("safety")
        # change do call install_with_constraints() instead of session.install()
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


# nox session for type check (mypy)
@nox.session(python=["3.8", "3.7"])
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


# nox session for type check (pytype)
@nox.session(python="3.7")
def pytype(session):
    """Run the static type checker."""
    # disable warnings for libraries / packages without type definitions
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


# define sessions run by default, excluding "black"
# i.e. do not run black and modify file(s) all the time
nox.options.sessions = "lint", "mypy", "pytype", "safety", "tests"
