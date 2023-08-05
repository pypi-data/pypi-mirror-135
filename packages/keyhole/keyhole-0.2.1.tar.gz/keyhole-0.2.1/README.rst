=======
keyhole
=======

A library and command-line tools for manipulating declassified imagery.

The primary use for this right now is mosaicking the separate "panel"
scans of declassified imagery from EarthExplorer.


Usage
=====

There are two steps to mosaick the panel images:

1.  Use the ``register`` subcommand to measure the panels' overlap. This
    will typically look something like::

        keyhole register -j coreg.json name_*.tif

    This will create ``coreg.json`` with the overlap information.

2.  Then use the ``mosaick`` subcommand with the information generated in the
    previous step to combine the images::

        keyhole mosaick -o output.tif -j coreg.json name_*.tif

The ``shrink`` argument is useful for creating smaller preview images::

    keyhole mosaick -o out.jpg --shrink 10 -j coreg.json name_*.tif

To create tiled pyramidal images::

    keyhole mosaick -o out.tif \
        --tile --pyramid --tile_width 256 --tile_height 256 \
        -j coreg.json name_*.tif

For more information, see ``keyhole -h``.


Installation
============

**Before installation**, you must have libvips installed. The procedure for
that varies by platform; see `the libvips documentation`__ for more info.
After that, simply::

    pip install keyhole

__ https://github.com/libvips/pyvips#non-conda-install

This installs both the package and the command-line tool ``keyhole``.

You can also run the code as a python module with ``python -m keyhole``.

If you've cloned the ``keyhole`` repo and you have the dependencies described
in ``pyproject.toml``, you can simply run the script at the root of the repo::

    python keyhole.py -h

