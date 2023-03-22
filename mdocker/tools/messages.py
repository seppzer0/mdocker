import sys


def note(msgtext):
    """A "note" wrapper."""
    print(f"[ * ] {msgtext}")


def error(msgtext, dont_exit=False):
    """An "error" wrapper."""
    print(f"[ ! ] {msgtext}", file=sys.stderr)
    if not dont_exit:
        sys.exit(1)


def done(msgtext):
    """A "done" wrapper."""
    print(f"[ + ] {msgtext}")


def cmd(msgtext):
    """A "cmd" wrapper."""
    print(f"[cmd] {msgtext}")
