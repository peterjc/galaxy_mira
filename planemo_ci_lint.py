#!/usr/bin/env python
"""Planemo Continuous Integration: Lint listed tools.

Currently no options.

Recurses under current directory to find Galaxy tools (which
we define as directories containing a valid ``.shed.yml`` file,
a much more narrow definition than planemo itself), writing
the list of tools to output file ``planemo_ci_all_tools.txt``
as plain text, one line per tool listing the relative directory.

The will deliberately check ``packages`` and ``datatypes``
before ``tools`` before ``workflows``, before other.

In essence, a more flexible version of this one-liner:

$ planemo shed_lint --report_level warn --tools --fail_level error `cat planemo_ci_all_tools.txt`

"""

import os
import sys

input_file = "planemo_ci_all_tools.txt"
output_file = "planemo_ci_valid_tools.txt"

def run_lint(tool_folder):
    """Runs planemo shed_lint

    Returns True there were no errors (warnings are OK).

    Returns False if there were errors.
    """
    cmd = "planemo shed_lint --report_level warn --tools --fail_level error %s" % tool_folder
    print(cmd)
    rc = os.system(cmd)
    print("planemo shed_lint returned %i for %s" % (rc, tool_folder))
    return not bool(rc)


total = 0
passed = 0
print("=" * 60)
print("Running planemo shed_lint to look for problems in tools...")
with open(input_file) as in_handle:
    with open(output_file, "w") as out_handle:
        for tool_folder in in_handle:
            total += 1
            tool_folder = tool_folder.strip()
            if not os.path.isfile(os.path.join(tool_folder, ".shed.yml")):
                sys.stderr.write("Missing %s\n" % os.path.join(tool_folder, ".shed.yml"))
            elif run_lint(tool_folder):
                passed += 1
                out_handle.write("%s\n" % tool_folder)
sys.stderr.write("Of %i tools in %s, %i passed planemo lint, saved to %s\n" % (total, input_file, passed, output_file))
