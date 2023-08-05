from inmanta.ast import RuntimeException


def assert_compilation_error(project, model, error_message):
    exception_occured = False
    try:
        project.compile(model)
    except RuntimeException as e:
        exception_occured = True
        assert error_message in e.msg
    assert exception_occured
