Galaxy wrapper for the MIRA assembly program (v4.9) mirabait
============================================================

This tool is copyright 2011-2015 by Peter Cock, The James Hutton Institute
(formerly SCRI, Scottish Crop Research Institute), UK. All rights reserved.
See the licence text below (MIT licence).

This is a Galaxy wrapper for ``mirabait`` from the MIRA 4.9 assembly suite.

It is available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/mira4_9_mirabait

Development/test previews are available from the Galaxy Test Tool Shed at:
http://testtoolshed.g2.bx.psu.edu/view/peterjc/mira4_9_mirabait

It is part of a suite for all the MIRA 4.9 tools:
TODO...

A separate wrapper for MIRA v4.0 is available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/peterjc/mira4_assembler


Automated Installation
======================

This should be straightforward. Via the Tool Shed, Galaxy should automatically
install the precompiled binaries for MIRA v4.9.5, and offer to run any tests.


Manual Installation
===================

There are various Python and XML files to install into Galaxy:

* ``mira4_9_mirabait.xml`` (the Galaxy tool definition for mirabait)
* ``mira_check_version.py`` (Python helper script)

The suggested location is a new ``tools/mira4_9`` folder. You will
also need to modify the ``tools_conf.xml`` file to tell Galaxy to offer the
tool::

  <tool file="mira4_9/mirabait/mira4_9_mirabait.xml" />
  ...

You will also need to install MIRA 4.9, we used version 4.9.5, and define the
environment variable ``$MIRA4_9`` pointing at the folder containing the
binaries. See:

* http://chevreux.org/projects_mira.html
* http://sourceforge.net/projects/mira-assembler/

You may wish to use different cluster setups for the de novo and mapping
tools, see above.

You will also need to install samtools (for generating a BAM file from MIRA's
SAM output).

If you wish to run the unit tests, also move/copy the ``test-data/`` files
under Galaxy's ``test-data/`` folder. Then::

    $ ./run_tests.sh -id mira4_9_mirabait
    ...


History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.1  - Initial version for MIRA 4.9.5, based on wrapper for v4.0.2
======= ======================================================================


Developers
==========

Development is on a dedicated GitHub repository:
https://github.com/peterjc/galaxy_mira/tree/master/tools/mira4_9

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff tools/mira4_9/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff tools/mira4_9/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only mira4_9/
    ...
    $ tar -tzf shed_upload.tar.gz 
    ...


Licence (MIT)
=============

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
