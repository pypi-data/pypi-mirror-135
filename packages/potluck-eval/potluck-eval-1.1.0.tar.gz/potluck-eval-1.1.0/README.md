# `potluck`

Code for automatically evaluating Python programming tasks, including a
`flask` WSGI server for handling submissions.

Specifications API design by Peter Mawhorter.

Server design by Peter Mawhorter, Scott Anderson, and Franklyn Turbak.

Based on `codder` program by Ben Wood w/ contributions by Franklyn Turbak
and Peter Mawhorter.


## Dependencies

The core evaluation code depends on the `jinja2`, `pygments`, `markdown`,
`importlib_resources`, `beautifulsoup4`, and `python_dateutil` packages.

Optional dependencies (get them using e.g., `python -m pip install
potluck-eval[test]`):

- `[test]`: Tests depend on `pytest`, and you can run them using `tox` if
    you want.
- `[expectations]`: Integration with `optimism` is available to require
    and grade student unit tests.
- `[turtle_capture]`: Full support for capturing `turtle` drawings
    requires the `Pillow` package (version 6.0.0 or later), as well as a
    Ghostscript installation (which is not simply a PyPI package and
    needs to be installed manually). Support for other image-producing
    code is possible, but would also require `Pillow`.
- `[synth]`: Integration with `wavesynth` is available for capturing
    audio produced by that package. Support for other audio libraries
    is not built in but is possible.
- `[server]`: If you want to run the `potluck_server` WSGI app, you'll
    need `flask` and `flask_cas`. If you're running the WSGI app on a
    server without a windowing system but still want to be able to
    evaluate submissions that use graphics (notably submissions which use
    the `turtle` module), there is support for using `xvfb-run` (which
    would have to be installed separately as it's not a PyPI package).
- `[security]` For full server security, you should also install
    `flask_talisman`, and `flask_seasurf`, but these are not required for
    running the server and won't be used if they're not present (although
    this introduces some extra security vulnerabilities).
- `[https_debug]` If you want to use a self-signed certificate for HTTPS
    while hosting the WSGI server locally for debugging purposes, you'll
    need `pyopenssl`. This is inconvenient, so it's not recommended
    unless you want to develop the server side of things.
- `[formatting]` For better formatting of markdown instructions,
   `pymarkdown-extensions` can be installed; it will be used if present,
   and the most important feature it provides is indented fenced code
   blocks so that they can be placed into list items.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python3 -m pip install potluck-eval
```

Confirm installation from within Python by running:

```py
>>> import potluck
```

Once that's done, you can perform run the built-in tests on the
command-line:

```sh
python -m potluck.tests
```

Note that if you get a command not found error, the `potluck_eval` script
might not have been installed somewhere that's on your command line's
path, which you'll need to fix to get the tests to run.

If you want to see what evaluation looks like yourself instead of just
running automated tests that clean up after themselves, in your installed
`potluck` directory inside of `site-packages` there's a `testarea`
directory; inside `testarea/test_course/fall2021` you should be able to
run the following commands:

```sh
potluck_eval -t functionsTest --rubric
potluck_eval -t functionsTest --instructions
potluck_eval -t functionsTest -u perfect
potluck_eval -t functionsTest -u imperfect
potluck_eval -t functionsTest --check
```

The first command creates a rubric for the "functionsTest" task in the
`rubrics` directory, and the second creates instructions in the
`instructions` directory. The third and fourth commands will evaluate the
provided test submissions for the same task, creating reports as
`reports/(im)perfect/functionsTest_TIMESTAMP.html` where TIMESTAMP is a
time-stamp based on when you run the command. The fifth command runs the
specification's built-in tests and prints out a report.

If the tests pass and these commands work, then `potluck` is properly
installed and you can start figuring out how to set up your own
evaluation area and define your own tasks. The documentation for the
`potluck.specifications` module describes the task-definition process and
provides a worked example that shows off many of the possibilities; you
can find that example specification at:

`potluck/testarea/test_course/fall2021/specs/functionsTest/spec.py`


## Evaluation Setup

Once `potluck` is installed and working , you'll need to set up your own
folder for evaluating submissions. The `potluck/testarea` folder contains
an example of this, including task specifications and example
submissions (note that it's missing a `submissions` folder because all of
its submissions are examples, as the `potluck_config.py` there notes).
You can test things out there, but eventually you'll want to create your
own evaluation directory, which should have at minimum:

- `tasks.json`: This file specifies which tasks exist and how to load
  their specifications, as well as which submitted files to look for and
  evaluate. You can work from the example in
  `potluck/testarea/test_course/fall2021/tasks.json`.
- A `specs` folder with one or more task sub-folders, named by their task
  IDs. Each task sub-folder should have a `spec.py` file that defines the
  task, as well as `starter/` and `soln/` folders which hold starter and
  solution code. These files and folders need to match what's specified
  in `tasks.json`.
- A `submissions` folder, with per-user submissions folders containing
  per-task folders that have actual submitted files in them. Note that if
  you're going to use the `potluck_server` WSGI app, this can be created
  automatically.

If you're going to use the `potluck_server` WSGI app, your evaluation
directory will also need:

- `potluck-admin.json`: Defines which users have admin privileges and
  allows things like masquerading and time travel. Work from the provided
  example `potluck/testarea/test_course/fall2021/potluck-admin.json`.

Finally, to run automated tests on your specifications (always a good
idea) you will need:

- An `examples` folder with the same structure as the `submissions`
  folder.


## Running `potluck_server`

To set up `potluck_server`, in addition to an evaluation directory set up
as described above, you'll need to create a `ps_config.py` file in a
directory of your choosing (could be the same as the base evaluation
directory if you want); there's a `rundir` directory inside the installed
`potluck_server` directory which has an example of this; in addition to
`ps_config.py`, `secret` and `syncauth` files will be created in the
server run-directory if not present.

For testing purposes, you will not need to change the `ps_config.py` file
from the defaults supplied in `ps_config.py.example`, but you'll want to
edit it extensively before running the server for real. When running in a
real WSGI context, you'll also need the `potluck.wsgi` file that's
present in the `potluck_server/rundir` directory.

Once `ps_config.py` has been created, from the `potluck_server/rundir`
directory (or whatever directory you set up) you should be able to run:

```py
python -m potluck_server.app
```

to run the WSGI app on a local port in debugging mode. It will print
several messages including one or more prompts about running without
authentication, and you'll have to press enter at these prompts to
actually start the server, after which it should provide you with a link
you can use in a browser to access it.

NOTE THAT THE POTLUCK WEB APP ALLOWS AUTHENTICATED USERS TO RUN ARBITRARY
PYTHON CODE ON THE SERVER!

In addition to this, in debugging mode the server has no authentication,
and is only protected by the fact that it's only accessible to localhost.
Accordingly, you will need to set up CAS (Central Authentication Server)
via the values in `ps_config.py` to run the server for real. If you don't
have access to a CAS instance via your company or institution, you can
either set one up yourself, or you'll have to modify the server to use
some other form of authentication. It is also *strongly* recommended that
you install the `flask_talisman` and `flask_seasurf` modules, which will
be used to provide additional security only if they're available. If
`pyopenssl` is installed alongside `flask_talisman`, a self-signed
certificate will be used to provide HTTPS even in debugging mode, mostly
just to maximize similarity between debugging & production environments.

In debugging mode, you will automatically be logged in as the "test"
user, and with the default `potluck-admin.json` file, this will be an
admin account, allowing you to do things like view full feedback before
the submission deadline is past. With the default setup, you should be
able to submit files for the testing tasks, and view the feedback
generated for those files (eventually, you may have to modify the due
dates in the example `tasks.json` for this to work). You can find files
to submit in the `potluck/testarea/test_course/fall2021/submissions`
directory, and you can always try submitting some of the solution files.

See the documentation at the top of `python_server/app.py` for a run-down
of how the server works and what's available.

To actually install the server as a WSGI app, you'll need to follow the
standard procedure for whatever HTTP server you're using. For example,
with Apache, this involves installing mod_wsgi and creating various
configuration files. An example Apache mod_wsgi configuration might look
like this (to be placed in `/etc/httpd/conf.d`):

```cfg
# ================================================================
# Potluck App for code submission & grading (runs potluck_eval)

# the following is now necessary in Apache 2.4; the default seems to be to deny.
<Directory "/home/potluck/private/potluck/potluck_server">
    Require all granted
</Directory>

WSGIDaemonProcess potluck user=potluck processes=5 display-name=httpd-potluck home=/home/potluck/rundir python-home=/home/potluck/potluck-python python-path=/home/potluck/rundir
WSGIScriptAlias /potluck /home/potluck/rundir/potluck.wsgi process-group=potluck
```


## Security

Running the potluck_server WSGI app on a public-facing port represents a
significant security vulnerability, since any authenticated user can
submit tasks, and the evaluation mechanisms currently do not use any
sandboxing, meaning that they RUN UNTRUSTED PYTHON CODE DIRECTLY ON YOUR
SERVER (even if they used sandboxing, which is a target feature for the
future, they would be vulnerable to any means of circumventing the
sandboxing used).

You therefore need to trust that your CAS setup is secure, and trust that
your users will be responsible about submitting files and about keeping
their accounts secure. If you can't depend on these things, DO NOT run
the web app.

Even if you do not run the web app, and instead collect submissions via
some other mechanism, the evaluation machinery still runs submitted code
directly. You will need to trust the users submitting tasks for
evaluation, and watch out for accidental mis-use of resources (e.g.,
creating files in an infinite loop). It's not a bad idea to run the
entire evaluation process in a virtual machine, although the details of
such a setup are beyond this document.


## Documentation

Extracted documentation can be viewed online at:
[https://cs.wellesley.edu/~pmwh/potluck/docs/potluck/](https://cs.wellesley.edu/~pmwh/potluck/docs/potluck/)

You can also read the same documentation in the docstrings of the source
code, or compile it yourself if you've got `make` and `pdoc` installed by
running the `make docs` script on the command-line (note that shenanigans
are necessary to prevent pdoc from trying to import the test
submissions).

## Changelog

- Version 1.0/1.1 brings potluck up-to-date with optimism 2.0, and adds a
  validation mode for checking test cases against solution code. Some
  improvements to resubmission and admin-based submission on the server
  are also included.
