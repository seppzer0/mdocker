import pytest

import mdocker.tools.messages as msg


def test__message_note__validate(capfd):
    """Check "note" message construction."""
    m = "This is a test message."
    expected_result = f"[ * ] {m}"
    msg.note(m)
    out, err = capfd.readouterr()
    assert out.replace("\n", "") == expected_result


@pytest.mark.parametrize("dont_exit", (False, True))
def test__message_error__validate(capfd, dont_exit: bool) -> None:
    """Check "error" message construction."""
    m = "This is a test message."
    expected_result = f"[ ! ] {m}"
    if dont_exit is False:
        with pytest.raises(SystemExit):
            msg.error(m, dont_exit)
    else:
        msg.error(m, dont_exit)
        out, err = capfd.readouterr()
        assert err.replace("\n", "") == expected_result


def test__message_done__validate(capfd) -> None:
    """Check "done" message construction."""
    m = "This is a test message."
    expected_result = f"[ + ] {m}"
    msg.done(m)
    out, err = capfd.readouterr()
    assert out.replace("\n", "") == expected_result


def test__message_cmd__validate(capfd) -> None:
    """Check "cmd" message construction."""
    m = "This is a test message."
    expected_result = f"[cmd] {m}"
    msg.cmd(m)
    out, err = capfd.readouterr()
    assert out.replace("\n", "") == expected_result
