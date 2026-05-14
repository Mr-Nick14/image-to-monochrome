Usage
=====

Installation
------------

.. code-block:: bash

   uv sync --extra dev

Basic run
---------

.. code-block:: bash

   uv run bw-converter ./input ./output --algorithm luminosity

Threshold run
-------------

.. code-block:: bash

   uv run bw-converter images result --algorithm threshold --threshold 120 --recursive --overwrite

Example output
--------------

.. code-block:: text

   Processed: 12; skipped: 1
   saved: result/photo.png
   skipped: images/readme.txt (Cannot read image: images/readme.txt)

Options
-------

``--algorithm``
   Conversion algorithm.

``--threshold``
   Binary threshold value from 0 to 255.

``--recursive``
   Process nested directories.

``--overwrite``
   Replace existing output files.

``--format``
   Output image format.

``--verbose``
   Print saved and skipped files.
