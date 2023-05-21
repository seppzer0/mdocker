import pytest
import mdocker.tools.messages as msg


def test__message_note__validate(capfd):
    """Check "note" message construction."""
    m = "This is a test message."
    expected_result = "[ * ] This is a test message."
    msg.note(m)
    out, err = capfd.readouterr()
    # remove trailing a "natural" newline
    assert out.replace("\n", "") == expected_result


@pytest.mark.parametrize(
    "dont_exit", [False, True]
)
def test__message_error__validate(capfd, dont_exit):
    """Check "error" message construction."""
    m = "This is a test message."
    expected_result = "[ ! ] This is a test message."
    if dont_exit is False:
        with pytest.raises(SystemExit):
            msg.error(m, dont_exit)
    else:
        msg.error(m, dont_exit)
        out, err = capfd.readouterr()
        # remove trailing a "natural" newline
        assert err.replace("\n", "") == expected_result


def test__message_done__validate(capfd):
    """Check "done" message construction."""
    m = "This is a test message."
    expected_result = "[ + ] This is a test message."
    msg.done(m)
    out, err = capfd.readouterr()
    # remove trailing a "natural" newline
    assert out.replace("\n", "") == expected_result


def test__message_cmd__validate(capfd):
    """Check "cmd" message construction."""
    m = "This is a test message."
    expected_result = "[cmd] This is a test message."
    msg.cmd(m)
    out, err = capfd.readouterr()
    # remove trailing a "natural" newline
    assert out.replace("\n", "") == expected_result
