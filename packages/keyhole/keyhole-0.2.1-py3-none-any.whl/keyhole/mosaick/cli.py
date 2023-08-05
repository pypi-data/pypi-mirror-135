import json
import pathlib
import sys

import numpy as np
import pyvips
import tqdm

from .mosaick import mosaick


description = """\
Mosaick images together according to a coregistration file.

The coregistration file is JSON with nested mappings, e.g.

    {
        "DS1000-01" : {
            "a" : [[...], [...], [...]],
            "b" : [[...], [...], [...]],
            ...
        },
        "DS1000-02" : ...
    }

The lists are a row-major transformation matrix M such that

    (r', c', 1) = M * (r, c, 1)

Where (r, c, 1) is a column vector of the row and column coordinates in the
original panel and (r', c', 1) is coordinates in the mosaicked image.

Note that any pixels projected to negative rows or columns are lost; the result
image is not moved right or down to accommodate them.
"""


def config_parser(parser):

    parser.add_argument(
        "--size",
        nargs=2,
        metavar=("num_rows", "num_cols"),
        type=int,
        help=(
            "Limit output size to the given dimensions. By default, expand"
            " the output image to accommodate the largest positive row and column."
        ),
    )

    parser.add_argument(
        "--shrink",
        metavar="scale",
        type=float,
        help="Reduce the output size by scale in both dimensions.",
    )

    parser.add_argument(
        "--rotate",
        action="store_true",
        help="Rotate the image 90° counter-clockwise.",
    )

    parser.add_argument(
        "--show-cols",
        action="store_true",
        help=(
            "Print the columns of the final image where the panels are"
            " joined. This is useful if you want to visually inspect the"
            " joins for artifacts."
        ),
    )

    parser.add_argument(
        "--tile",
        action="store_true",
        help="Write a tiled tiff.",
    )

    parser.add_argument(
        "--tile_width",
        type=int,
        help="Tile width in pixels",
    )

    parser.add_argument(
        "--tile_height",
        type=int,
        help="Tile height in pixels",
    )

    parser.add_argument(
        "--pyramid",
        action="store_true",
        help="Write a pyramidal tiff.",
    )

    parser.add_argument(
        "-j",
        "--coreg-json",
        metavar="coreg_file",
        type=pathlib.Path,
        help="A JSON file with coregistration information.",
        required=True,
        dest="coreg",
    )

    parser.add_argument(
        "panels",
        metavar="panel_file",
        nargs="+",
        type=pathlib.Path,
        help="Panel image files from a single declass image.",
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="output_file",
        type=pathlib.Path,
        help="Output image.",
        required=True,
    )


def cli(args):
    image_names = [parse_declass_name(path)[0] for path in args.panels]
    image_name = image_names[0]
    if not all(name == image_name for name in image_names):
        sys.exit("Specified panel files belong to more than one image.")

    panel_data = {}
    for path in args.panels:
        _, panel_letter = parse_declass_name(path)
        panel_data[panel_letter] = pyvips.Image.new_from_file(str(path))

    # Load transforms for the given image.
    with open(args.coreg) as json_file:
        j = json.load(json_file)[image_name]
        panel_tforms = {panel: np.asarray(j[panel]) for panel in j}

    # Determine the order of the panels in the final image by sorting based on
    # their horizontal offset.
    panel_order = sorted(panel_tforms, key=lambda p: panel_tforms[p][1, 2])
    panels = [panel_data[p] for p in panel_order]
    tforms = [panel_tforms[p] for p in panel_order]

    result, split_columns = mosaick(panels, tforms)

    if args.size:
        num_rows, num_cols = args.size
        result = result.crop(0, 0, num_cols, num_rows)

    if args.rotate:
        result = result.rot270()

    if args.shrink:
        result = result.resize(1.0 / args.shrink)

    if args.show_cols:
        print("Split columns:", split_columns)

    if args.tile or args.pyramid:
        tiff_args = {
            k: vars(args)[k]
            for k in ["tile", "tile_width", "tile_height", "pyramid"]
            if k in vars(args)
        }
    else:
        tiff_args = {}

    write_with_progress(result, args.output, tiff_args)


def parse_declass_name(path):
    "Get the image and panel names from a declassified image path."
    stem = path.stem
    if stem[-2] != "_":
        raise ValueError(f"{str(path)} isn't named <image>_<panel>.tif")
    return stem[:-2], stem[-1]


def write_with_progress(image, path, write_args=None):
    """Write a VIPS image while showing a progress bar."""
    write_args = {} if write_args is None else write_args

    class ProgressBar(tqdm.tqdm):
        def vips_update(self, _, progress):
            self.total = progress.tpels
            return self.update(progress.npels - self.n)

    if path.suffix.lower() in [".tif", ".tiff"]:
        write_args["bigtiff"] = True

    with ProgressBar(desc="Mosaicking", bar_format="{l_bar}{bar}|{elapsed}") as t:
        image.set_progress(True)
        image.signal_connect("preeval", t.vips_update)
        image.signal_connect("eval", t.vips_update)
        image.signal_connect("posteval", t.vips_update)
        image.write_to_file(str(path), **write_args)
