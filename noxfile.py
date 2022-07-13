from nox_poetry import session


@session(python="3.10")
def tests(session):
    """ Running tests """
    session.run("pytest")

