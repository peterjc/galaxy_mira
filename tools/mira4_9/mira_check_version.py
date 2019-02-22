#!/usr/bin/env python
"""A simple wrapper script to call a MIRA binary to check/report its version.

Syntax: mira_check_version.py binary [expected pattern]

The binary can be a full path, otherwise ``$PATH`` is searched as normal.

Example output from MIRA V3.4 suite installed on the ``$PATH``::

    $ python mira_check_version.py mira
    This is MIRA V3.4.1.1 (production version).
    $ python mira_check_version.py mirabait
    V3.4.1.1

Example output from MIRA v4.0.2::

    $ python mira_check_version.py ~/downloads/mira_4.0.2_linux-gnu_x86_64_static/bin/mira
    4.0.2
    $ python mira_check_version.py ~/downloads/mira_4.0.2_linux-gnu_x86_64_static/bin/mirabait
    4.0.2
    $ python mira_check_version.py ~/downloads/mira_4.0.2_linux-gnu_x86_64_static/bin/miraconvert
    4.0.2

Example output from MIRA v4.9.5::

    $ python mira_check_version.py ~/downloads/mira_4.9.5_2_linux-gnu_x86_64_static/bin/mira
    4.9.5_2
    $ python mira_check_version.py ~/downloads/mira_4.9.5_2_linux-gnu_x86_64_static/bin/mirabait
    4.9.5_2
    $ python mira_check_version.py ~/downloads/mira_4.9.5_2_linux-gnu_x86_64_static/bin/miraconvert
    4.9.5_2

The optional version checking is simple substring approach (beware of potential
issues if MIRA versions ever use double digits for minor version), and returns
zero if this matched::

    $ python mira_check_version.py mirabait 4.9 ; echo "Return value $?"
    4.9.5_2
    Return value 0

If the expected version did not match, the return value is one (error)::

    $ python mira_check_version.py mirabait 4.9 ; echo "Return value $?"
    Expected MIRA v4.9, but mirabait reports: V3.4.1.1
    Return value 1

This script is intended to be used as part of my Galaxy wrappers for MIRA,
where it will capture and record the version used - and give a clear error
message if there is a version mismatch (otherwise due to API changes the
MIRA error messages tend to be very long and somewhare confusing).
"""

from __future__ import print_function

import subprocess
import sys

WRAPPER_VER = "0.0.2"  # Keep in sync with the XML file


def get_version(mira_binary):
    """Run MIRA to find its version number."""
    # At the commend line I would use: mira -v | head -n 1
    # however there is some pipe error when doing that here.
    cmd = [mira_binary, "-v"]
    try:
        child = subprocess.Popen(
            cmd,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as err:
        sys.stderr.write("Error invoking command:\n%s\n\n%s\n" % (" ".join(cmd), err))
        sys.exit(1)
    ver, tmp = child.communicate()
    del child
    # Workaround for -v not working in mirabait 4.0RC4
    if "invalid option" in ver.split("\n", 1)[0]:
        for line in ver.split("\n", 1):
            if " version " in line:
                line = line.split()
                return line[line.index("version") + 1].rstrip(")")
        sys.exit("Could not determine MIRA version:\n%s" % ver)
    return ver.split("\n", 1)[0]


if "-v" in sys.argv or "--version" in sys.argv:
    print("mira_check_version.py version %s" % WRAPPER_VER)
    sys.exit(0)

if len(sys.argv) == 2:
    mira_binary = sys.argv[1]
    expected = None
elif len(sys.argv) == 3:
    mira_binary = sys.argv[1]
    expected = sys.argv[2]
else:
    sys.exit("Usage: mira_check_version.py mira_binary [expected version]")

mira_ver = get_version(mira_binary)
if expected and not mira_ver.strip().startswith(expected):
    sys.exit(
        "Expected MIRA v%s, but %s reports: %s" % (expected, mira_binary, mira_ver)
    )
print(mira_ver)
