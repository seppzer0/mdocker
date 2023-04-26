import subprocess
import mdocker.tools.messages as msg


def cmdd(cmd, quiet=False, dont_exit=False):
    """
    A simple (Docker) command wrapper.

    :param str cmd: A command that is being executed.
    :param bool quiet: Omit command printout.
    :param bool dont_exit: Do not exit program if an error occured.
    """
    if not quiet:
        msg.cmd(cmd)
    # determine stdout
    cstdout = subprocess.DEVNULL if quiet else None
    rc = subprocess.run(cmd, stdout=cstdout, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        msg.error("Could not launch: {}".format(cmd), dont_exit)
