import subprocess
import mdocker.tools.messages as msg


def cmdd(cmd: str, quiet: bool = False, dont_exit: bool = False):
    """A simple (Docker) command wrapper.

    :param str cmd: A command that is being executed.
    :param bool quiet: Omit command printout.
    :param bool dont_exit: Do not exit program if an error occured.
    """
    if not quiet:
        msg.cmd(cmd)
    # determine stdout
    cstdout = subprocess.DEVNULL if quiet else None
    try:
        subprocess.run(cmd.split(" "), check=True, stdout=cstdout, stderr=subprocess.STDOUT)
    except Exception:
        msg.error(f"Could not launch: {cmd}", dont_exit)
