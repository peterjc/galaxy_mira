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

output_file = "planemo_ci_all_tools.txt"
short_list = ["packages", "datatypes", "tools", "workflows"]

# TODO: Consider using glob, or os.walk here?
def recurse_folder_for_tools(folder):
    for f in os.listdir(folder):
        full = os.path.join(folder, f)
        if f == ".shed.yml" and os.path.isfile(full):
            yield folder
        elif os.path.isdir(full):
            # TODO: Yield from
            for child in recurse_folder_for_tools(full):
                yield child

def find_tools(short_list):
    for f in short_list:
        if os.path.isdir(f):
            # TODO: yield from
            for tool_folder in recurse_folder_for_tools(f):
                yield tool_folder
    # Check if there are any non-canonical folders in use...
    # TODO: Give a warning or error here?
    for f in os.listdir("."):
        if os.path.isdir(f) and f not in short_list:
            for tool_folder in recurse_folder_for_tools(f):
                yield tool_folder


print("=" * 60)
print("Indentifying Galaxy tools with planemo .shed.yml files...")

tools = list(find_tools(short_list))
with open("planemo_ci_all_tools.txt", "w") as output:
    for tool_folder in tools:
         assert os.path.isfile(os.path.join(tool_folder, ".shed.yml"))
         print(tool_folder)
         output.write("%s\n" % tool_folder)

sys.stderr.write("Found %i tools, saved to %s\n" % (len(tools), output_file))
