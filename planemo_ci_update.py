#!/usr/bin/env python
"""Planemo Continuous Integration: Update listed tools on Tool Shed.

Currently no options. Roughly equivalent to this one-liner:

$ planemo shed_update --fail_fast --force_repository_creation $(cat planemo_ci_tested.txt)

"""

import os
import sys

input_file = "planemo_ci_tested_tools.txt"
output_file = "planemo_ci_updated_tools.txt"
tool_shed = "testtoolshed"

def push_to_tool_shed(tool_folder):
    """Runs planemo shed_update

    Returns True if changes were uploaded (including creating the repo).

    Returns False if there were no changes, or an error occured.
    """
    cmd = "planemo shed_update -t %s --fail_fast --force_repository_creation %s" % (tool_shed, tool_folder)
    print(cmd)
    rc = os.system(cmd)
    print("planemo shed_update returned %i for %s" % (rc, tool_folder))
    return not bool(rc)

total = 0
updated = 0
print("=" * 60)
print("Running planemo shed_upload to update tested tools...")
with open(input_file) as in_handle:
    with open(output_file, "w") as out_handle:
        for tool_folder in in_handle:
            total += 1
            tool_folder = tool_folder.strip()
            if not os.path.isfile(os.path.join(tool_folder, ".shed.yml")):
                sys.stderr.write("Missing %s\n" % os.path.join(tool_folder, ".shed.yml"))
            elif push_to_tool_shed(tool_folder):
                updated += 1
                out_handle.write("%s\n" % tool_folder)
sys.stderr.write("Of %i tools in %s, %i updated on %s, saved to %s\n" % (total, input_file, updated, tool_shed, output_file))

