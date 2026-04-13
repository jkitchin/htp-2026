# htp

`htp` is a small Python 3 package of high-throughput helpers: running
commands on a remote host via `ssh`, and sending email over SMTP with or
without a file attachment. It is a modernized slice of the original
[htp](https://github.com/jkitchin/htp) project, ported from Python 2 and
reduced to two well-scoped utilities.

## Installing

From a clone of the repository:

```sh
uv sync
```

or, to install into an existing environment:

```sh
uv pip install .
```

## What is documented here

The notebooks below walk through each submodule, one function at a time,
with runnable examples. The examples are shown as code but are not
executed when the book is built, because they require a live SSH target
and a reachable SMTP server.

- [Running remote commands with `htp.ssh`](ssh.ipynb)
- [Sending email with `htp.mail`](mail.ipynb)
