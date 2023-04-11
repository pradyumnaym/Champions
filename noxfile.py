# from tempfile import NamedTemporaryFile

import nox
from nox_poetry import Session, session

# nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["fmt_check", "lint", "test"]


@session(python=["3.10"])
def test(s: Session) -> None:
    s.install(".", "pytest", "pytest-cov")
    s.run(
        "python",
        "-m",
        "pytest",
        "--junitxml=junit/test-results.xml",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=xml",
        *s.posargs,
    )


# For some sessions, set venv_backend="none" to simply execute scripts within the existing Poetry
# environment. This requires that nox is run within `poetry shell` or using `poetry run nox ...`.


@session(venv_backend="none")
def fmt_check(s: Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@session(venv_backend="none")
def lint(s: Session) -> None:
    # Run pyproject-flake8 entrypoint to support reading configuration from pyproject.toml.
    s.run("pflake8")


# @session(venv_backend="none")
# def type_check(s: Session) -> None:
#     s.run("mypy", "app", "tests", "noxfile.py")
