Algorithms
==========

average
-------

Uses the arithmetic mean of RGB channels:

.. math::

   gray = (R + G + B) / 3

luminosity
----------

Uses weighted RGB channels. This usually looks more natural for human vision:

.. math::

   gray = 0.299R + 0.587G + 0.114B

threshold
---------

First calculates grayscale value, then converts the pixel to black or white:

.. math::

   pixel = 255 \text{ if } gray >= threshold \text{ else } 0

max_channel
-----------

Uses the largest RGB channel value.

min_channel
-----------

Uses the smallest RGB channel value.
