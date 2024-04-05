import subprocess
from typing import Optional

import mdocker.tools.messages as msg


def launch(
        cmd: str,
        quiet: Optional[bool] = False,
        dont_exit: Optional[bool] = False,
        get_output: Optional[bool] = False
    ) -> subprocess.CompletedProcess | str | None:
    """A simple command wrapper.

    :param cmd: A command that is being executed.
    :param quiet: Omit command printout.
    :param dont_exit: Do not exit program if an error occured.
    :param get_output: A switch to get the piped output of the command.
    """
    # optionally print the command
    if not quiet:
        print(f"[cmd] {cmd}")
    # determine stdout
    cstdout = subprocess.DEVNULL if quiet else None
    if get_output is True:
        cstdout = subprocess.PIPE
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=cstdout, stderr=subprocess.STDOUT)
        # return only output if required
        if get_output is True:
            return result.stdout.decode("utf-8").rstrip()
        else:
            return result
    except Exception:
        if not dont_exit:
            msg.error(f"Error executing command: {cmd}")
