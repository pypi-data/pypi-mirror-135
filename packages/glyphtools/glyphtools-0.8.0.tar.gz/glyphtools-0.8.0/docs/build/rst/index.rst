
Welcome to glyphtools’s documentation!
**************************************

**glyphtools.bin_glyphs_by_metric(font, glyphs, category,
bincount=5)**

   Organise glyphs according to a given metric.

   Organises similar glyphs into a number of bins. The bins are not
   guaranteed to contain the same number of glyphs; the
   one-dimensional ckmeans clustering algorithm is used to cluster
   glyphs based on metric similarity. For example, if there are five
   glyphs of width 100, 102, 105, 210, and 220 units respectively, and
   you ask for two bins, the first bin will contain three glyphs and
   the second will contain two. This is usually what you want.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **glyphs** – a collection of glyph names

      * **category** – the metric (see metric keys in
         `get_glyph_metrics()`_.)

      * **bincount** – number of bins to return

   :Returns:
      A list of ``bincount`` two-element tuples. The first element is
      a list of glyphnames in this bin; the second is the average
      metric value of the glyphs in this bin.

**glyphtools.categorize_glyph(font, glyphname)**

   Returns the category of the given glyph.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **glyphname** – name of the glyph.

   :Returns:
      A two-element tuple. The first element is one of the following
      strings: ``unknown``, ``base``, ``mark``, ``ligature``,
      ``component``. If the glyph is a mark, the second element is the
      mark attachment class number.

**glyphtools.determine_kern(font, glyph1, glyph2, targetdistance,
offset1=0, 0, offset2=0, 0, maxtuck=0.4)**

   Determine a kerning value required to set two glyphs at given
   ink-to-ink distance.

   The value is bounded by the ``maxtuck`` parameter. For example, if
   ``maxtuck`` is 0.20, the right glyph will not be placed any further
   left than 80% of the width of left glyph, even if this places the
   ink further than ``targetdistance`` units away.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **glyph1** – name of the left glyph.

      * **glyph2** – name of the right glyph.

      * **targetdistance** – distance to set the glyphs apart.

      * **offset1** – offset (X-coordinate, Y-coordinate) to place
         left glyph.

      * **offset2** – offset (X-coordinate, Y-coordinate) to place
         right glyph.

      * **maxtuck** – maximum proportion of the left glyph’s width to
         kern.

   Returns: A kerning value, in units.

**glyphtools.duplicate_glyph(font, existing, new)**

   Add a new glyph to the font duplicating an existing one.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **existing** – name of the glyph to duplicate.

      * **new** – name of the glyph to add.

**glyphtools.get_glyph_metrics(font, glyphname)**

   Returns glyph metrics as a dictionary.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **glyphname** – name of the glyph.

   :Returns:
      width: Advance width of the glyph. lsb: Left side-bearing rsb:
      Right side-bearing xMin: minimum X coordinate xMax: maximum X
      coordinate yMin: minimum Y coordinate yMax: maximum Y coordinate
      rise: difference in Y coordinate between cursive entry and exit

   :Return type:
      A dictionary with the following keys

**glyphtools.set_glyph_category(font, glyphname, category,
maClass=None)**

   Sets the category of the glyph in the font.

   :Parameters:
      * **font** – a ``fontTools`` TTFont object.

      * **glyphname** – name of the glyph.

      * **category** – one of ``base``, ``mark``, ``ligature``,
         ``component``.

      * **maClass** – If the category is ``base``, the mark
         attachment class number.


Installation
============


Stable release
--------------

To install glyphtools, run this command in your terminal:

::

   $ pip install glyphtools

This is the preferred method to install glyphtools, as it will always
install the most recent stable release.

If you don’t have `pip <https://pip.pypa.io>`_ installed, this `Python
installation guide
<http://docs.python-guide.org/en/latest/starting/installation/>`_ can
guide you through the process.


From sources
------------

The sources for glyphtools can be downloaded from the `Github repo
<https://github.com/simoncozens/glyphtools>`_.

You can either clone the public repository:

::

   $ git clone git://github.com/simoncozens/glyphtools

Or download the `tarball
<https://github.com/simoncozens/glyphtools/tarball/master>`_:

::

   $ curl -OJL https://github.com/simoncozens/glyphtools/tarball/master

Once you have a copy of the source, you can install it with:

::

   $ python setup.py install


Usage
=====

To use glyphtools in a project:

::

   import glyphtools
