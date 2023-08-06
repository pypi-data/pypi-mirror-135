setuputils3
===========

A utility module to automate building setup configuration files.
The latest official release is available on PyPI at
https://pypi.org/project/setuputils3/
and the latest source code is available on Gitlab at
https://gitlab.com/pdonis/setuputils3.

Running ``setuputils`` in the root of your source tree will build
a ``setup.cfg`` file for you from inputs that you supply and from
its ability to auto-discover the things that typically go into a
distribution of your Python application or library. The main tool
that uses ``setup.cfg``, ``setuptools``, also has much the same
auto-discovery capability, but the advantage with ``setuputils`` is
that you get to see all the output of the auto-discovery logic in
the final ``setup.cfg`` file *before* using it to build your
distribution. With ``setuptools``, you have no way of getting an
advance look at what the tool thinks should go into your
distribution; you only see what is in the distribution after it
is built.

Using setuputils in this mode is simple: for each section of
``setup.cfg``, you put options that you want to specify in advance
in the root of your source tree in files with an ``.in`` extension,
one for each section that will end up in ``setup.cfg``. For example,
you would put metadata in the file ``metadata.in``, options in the
file ``options.in``, etc. You would not include anything that you want
``setuputils`` to auto-discover, so, for example, if you want
``setuputils`` to auto-discover your packages, you would not include
"packages" in your ``options.in`` file at all (whereas with
``setuptools`` you would include "packages = find:" in your
``setup.cfg``).

Once you have created your ``.in`` files, then you simply execute

    $ python3 -m setuputils

in the root of your source tree. This will build the ``setup.cfg``
file for you. You can then look at it to make sure it is correct
before using a build backend to build your distribution.

With this mode, if you are using a PEP 517 compliant build backend, you
do not need a ``setup.py`` script at all. (``Setuptools`` qualifies as
such a backend as long as you include a ``pyproject.toml file`` and specify
``setuptools`` in it, as described in the Python packaging documentation.)
If you do have a ``setup.py`` script, all it would need to contain is
an import of ``setuptools`` and call to ``setuptools.setup()`` with no
arguments (since all of the information needed is in ``setup.cfg``).

Note, however, that if you have a ``setup.py`` script that was used with
previous versions of ``setuputils``, you do not have to transition it to the
new format using ``.in`` files all at once. ``Setuputils`` will read any
global variables that are defined in your ``setup.py``, as you would have
done in previous ``setuputils versions``, and include them in what it
outputs to ``setup.cfg`` after processing them just as it would have in
previous versions, so you can transition things incrementally if that works
better for your project. (However, you should remove any calls to
``setup_vars`` in your ``setup.py`` script, leaving only the call to
``setuptools.setup()`` with no arguments, since all the information
it needs will be in ``setup.cfg``.)

See the module docstrings for more information.

SETUPUTILS3 is Copyright (C) 2012-2022 by Peter A. Donis.
Released under the Python Software Foundation License.
