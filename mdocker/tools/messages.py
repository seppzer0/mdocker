import sys


def note(msgtext):
    """A "note" text wrapper."""
    print(f"[ * ] {msgtext}")


def error(msgtext, dont_exit=False):
    """An "error" text wrapper."""
    print(f"[ ! ] {msgtext}", file=sys.stderr)
    if not dont_exit:
        sys.exit(1)


def done(msgtext):
    """A "done" text wrapper."""
    print(f"[ + ] {msgtext}")


def cmd(msgtext):
    """A "cmd" text wrapper."""
    print(f"[cmd] {msgtext}")
