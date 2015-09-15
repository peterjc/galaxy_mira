#!/usr/bin/env python
"""Planemo Continuous Integration: Summary of progress

Currently no options. Call this after:
 - ./planemo_ci_find.py
 - ./planemo_ci_lint.py
 - ./planemo_ci_diff.py
 - ./planemo_ci_test.py

Expect to call planemo_ci_update.py if the report passes.
"""

import sys
import os

all_file = "planemo_ci_valid_tools.txt"
valid_file = "planemo_ci_valid_tools.txt"
changed_file = "planemo_ci_changed_tools.txt"
tested_file = "planemo_ci_tested_tools.txt"
#After this script, will produce this:
#updated_file = "planemo_ci_updated_tools.txt"


def load_list(filename):
    with open(filename) as handle:
        for line in handle:
            tool_folder = line.strip()
            if tool_folder:
                yield tool_folder


valid = set(load_list(valid_file))
changed = set(load_list(changed_file))
tested = set(load_list(tested_file))
fail = False
print("=" * 60)
print("Summary of Galaxy tools with planemo .shed.yml files...")
for tool in load_list(all_file):
    if tool not in valid:
        print(" - %s - ERROR - failed linting" % tool)
        fail = True
    elif tool not in changed:
        print(" - %s - has not changed, not tested" % tool)
    elif tool not in tested:
        print(" - %s - ERROR - failed testing" % tool)
        fail = True
    else:
        print(" - %s - updated and tests passed" % tool)

if fail:
    # One or more errors, do not do Tool Shed upload
    # (right now we have no dependency chain information)
    sys.exit(1)
