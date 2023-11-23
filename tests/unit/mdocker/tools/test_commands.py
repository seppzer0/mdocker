import pytest

import mdocker.tools.commands as ccmd


def test__cmdd__validate(capfd) -> None:
    """Test an invalid command execution handling."""
    cmd = "some_invalid_command"
    with pytest.raises(SystemExit):
        ccmd.launch(cmd)
