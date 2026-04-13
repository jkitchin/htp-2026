"""Run commands on a remote host via ssh."""

import subprocess


class SSHError(Exception):
    """Raised when an ssh invocation exits with a non-zero status."""


def ssh(cmds, host, ssh_cmd=("ssh", "-x")):
    """Run one or more commands on a remote host via ssh.

    Parameters
    ----------
    cmds : str or iterable of str
        Command to execute remotely. If an iterable of strings is
        given, its elements are joined with ``"; "`` and sent as a
        single remote command.
    host : str
        SSH target, for example ``"user@host.example.com"`` or
        ``"host.example.com"``.
    ssh_cmd : sequence of str, optional
        The ssh executable and its flags, passed as the leading
        elements of the argv list. Defaults to ``("ssh", "-x")``.

    Returns
    -------
    status : int
        Exit status of the remote command. Always ``0`` on success.
    output : str
        Combined stdout and stderr produced by the remote command.

    Raises
    ------
    SSHError
        If the remote command returns a non-zero exit status.
    """
    if isinstance(cmds, str):
        remote = cmds
    else:
        remote = "; ".join(cmds)

    argv = [*ssh_cmd, host, remote]
    result = subprocess.run(argv, capture_output=True, text=True)
    output = result.stdout + result.stderr

    if result.returncode != 0:
        raise SSHError(
            f"ssh to {host} failed with status {result.returncode}\n"
            f"argv: {argv}\n"
            f"output:\n{output}"
        )

    return result.returncode, output
