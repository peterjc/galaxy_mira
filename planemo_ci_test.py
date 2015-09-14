#!/usr/bin/env python
"""Planemo Continuous Integration: Update listed tools on Tool Shed.

Currently no options. Roughly equivalent to this one-liner:

$ planemo shed_test $(cat planemo_changed_tools.txt)

"""

import os
import sys

input_file = "planemo_ci_changed_tools.txt"
output_file = "planemo_ci_tested_tools.txt"

def test_tool(tool_folder):
    """Runs planemo test

    Returns True if tests pass.

    Returns False if tests fail, or an error occured.
    """
    cmd = "planemo test %s" % tool_folder
    print(cmd)
    rc = os.system(cmd)
    print("planemo test returned %i for %s" % (rc, tool_folder))
    return not bool(rc)

total = 0
passed = 0
print("=" * 60)
print("Running planemo test to validate updated tools...")
with open(input_file) as in_handle:
    with open(output_file, "w") as out_handle:
        for tool_folder in in_handle:
            total += 1
            tool_folder = tool_folder.strip()
            if not os.path.isfile(os.path.join(tool_folder, ".shed.yml")):
                sys.stderr.write("Missing %s\n" % os.path.join(tool_folder, ".shed.yml"))
            elif test_tool(tool_folder):
                passed += 1
                out_handle.write("%s\n" % tool_folder)
sys.stderr.write("Of %i tools, %i passed testes, saved to %s\n" % (total, passed, output_file))
#if passed < total:
#    sys.stderr.write("ERROR: Some tools failed linting.\n")
#    sys.exit(1)
