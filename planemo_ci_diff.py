#!/usr/bin/env python
"""Planemo Continuous Integration: Compare with tools on Tool Shed.

Currently no options. Roughly equivalent to this one-liner:

$ planemo shed_diff -t testtoolshed $(cat planemo_ci_valid_tools.txt)

but capturing a list of the changed tools.
"""

import os
import sys

input_file = "planemo_ci_valid_tools.txt"
output_file = "planemo_ci_changed_tools.txt"
tool_shed = "testtoolshed"

def compare_to_tool_shed(tool_folder):
    """Runs planemo shed_diff

    Returns True if changes exist (or has not been uploaded yet)
    TODO - https://github.com/galaxyproject/planemo/issues/300

    Returns False if there were no changes, or an error occured.
    """
    cmd = "planemo shed_diff -t %s --fail_fast %s > /dev/null" % (tool_shed, tool_folder)
    rc = os.system(cmd)
    # Expect 0 = no changes, 1 = changes, other = error
    # print("planemo shed_diff on %s returned %i for %s" % (tool_shed, rc, tool_folder))
    # Seems get 0 = no changes, other = changes/error
    # e.g. 255
    return bool(rc)

total = 0
changed = 0
print("=" * 60)
print("Running planemo shed_diff to look for updated tools...")
with open(input_file) as in_handle:
    with open(output_file, "w") as out_handle:
        for tool_folder in in_handle:
            total += 1
            tool_folder = tool_folder.strip()
            if not os.path.isfile(os.path.join(tool_folder, ".shed.yml")):
                sys.stderr.write("Missing %s\n" % os.path.join(tool_folder, ".shed.yml"))
            elif compare_to_tool_shed(tool_folder):
                changed += 1
                print(" - changes in %s" % tool_folder)
                out_handle.write("%s\n" % tool_folder)
sys.stderr.write("Of %i tools in %s, %i changed vs %s, saved to %s\n" % (total, input_file, changed, tool_shed, output_file))
