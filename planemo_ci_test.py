#!/usr/bin/env python
"""Planemo Continuous Integration: Update listed tools on Tool Shed.

Currently no options. Roughly equivalent to this one-liner:

$ planemo shed_test $(cat planemo_changed_tools.txt)

"""

import os
import sys
import time

input_file = "planemo_ci_changed_tools.txt"
output_file = "planemo_ci_tested_tools.txt"

try:
    galaxy_root = os.environ["GALAXY_ROOT"]
except KeyError:
    sys.stderr.write("Missing $GALAXY_ROOT environment variable.")
    sys.exit(1)

def test_tool(tool_folder):
    """Runs planemo test

    Returns True if tests pass (and hides stdout/stderr).

    Returns False if tests fail, or an error occured, and
    will show the verbose stdout/stderr to see the error.
    """
    terminal_output = "%s/.planemo_test.log" % tool_folder
    text_output = "%s/.planemo_test.txt" % tool_folder
    md_output = "%s/.planemo_test.md" % tool_folder
    cmd = "planemo test --galaxy_root %s --tool_test_output_text %s --tool_test_output_markdown %s %s &> %s" \
        % (galaxy_root, text_output, md_output, tool_folder, terminal_output)
    print(cmd)
    start = time.time()
    rc = os.system(cmd)
    taken = time.time() - start
    print("planemo test returned %i for %s (%0.02fs)" % (rc, tool_folder, taken))
    if rc:
        # Hope will be able to use just one of these in future...
        os.system("cat %s" % text_output)
        os.system("cat %s" % md_output)
        os.system("cat %s" % terminal_output)  # very long
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
