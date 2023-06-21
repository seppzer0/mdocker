import subprocess
from typing import Union

import mdocker.tools.messages as msg


def launch(cmd, quiet=False, dont_exit=False, get_output=False) -> Union[None, str]:
    """A simple (Docker) command wrapper.

    :param str cmd: A command that is being executed.
    :param bool quiet: Omit command printout.
    :param bool dont_exit: Do not exit program if an error occured.
    """
    if not quiet:
        msg.cmd(cmd)
    # determine stdout
    cstdout = subprocess.DEVNULL if quiet else None
    if get_output is True:
        cstdout = subprocess.PIPE
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=cstdout, stderr=subprocess.STDOUT)
        # return only output if required
        if get_output is True:
            return result.stdout.decode('utf-8').splitlines()[0]
    except Exception:
        msg.error(f"Error executing command: {cmd}")
