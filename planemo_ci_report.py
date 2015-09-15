#!/usr/bin/env python
"""Planemo Continuous Integration: Find all tools.

Currently no options.

Expects list of tool folders via stdin (one line per tool,
listing folder name containing a ``.shed.yml`` file).

Calls ``planemo lint`` on each tool, producing two output
files.

Recurses under current directory to find Galaxy tools (which
we define as directories containing a valid ``.shed.yml`` file,
a much more narrow definition than planemo itself), writing
the list of tools to output file ``planemo_ci_all_tools.txt``
and stdout as plain text, one line per tool listing the
relative directory.

The will deliberately check ``packages`` and ``datatypes``
before ``tools`` before ``workflows``, before other.

In essence, a more flexible version of this one-liner:

$ ls -1 packages/*/.shed.yml datatypes/*/.shed.yml tools/*/.shed.yml workflows/*/.shed.yml
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
        print(" - %s - has not changed" % tool)
    elif tool not in tested:
        print(" - %s - ERROR - failed testing" % tool)
        fail = True
    else:
        print(" - %s - updated and tests passed" % tool)

if fail:
    # One or more errors, do not do Tool Shed upload
    # (right now we have no dependency chain information)
    sys.exit(1)
