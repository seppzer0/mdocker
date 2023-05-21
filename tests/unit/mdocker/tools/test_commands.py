import pytest
from mdocker.tools.commands import cmdd


@pytest.mark.parametrize(
    "cmd, quiet",
    [
        ("falseecho", True),
        ("falseecho", False)
    ]
)
def test__cmdd__validate(capfd, cmd, quiet):
    """Test false command launch mechanism."""
    expected_result = f"[cmd] {cmd}" if not quiet else ""
    if "falseecho" in cmd and not quiet:
        with pytest.raises(SystemExit):
            cmdd(cmd, quiet)
