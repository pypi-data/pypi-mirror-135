from collections import namedtuple

import numpy as np
import pyvips


def apply_tform(tform, coords):
    """Apply a transformation matrix to (row, col) coordinates."""
    src = np.concatenate([coords, np.ones((len(coords), 1))], axis=1)
    dst = (tform @ src.T).T
    dst[:, :2] /= dst[:, 2:3]
    return dst[:, :2]


def get_tformed_corners(tform, image):
    """Get the corners of an image after they've been transformed."""
    upper, lower = 0, image.height - 1
    left, right = 0, image.width - 1
    corners = np.array([[upper, left], [upper, right], [lower, right], [lower, left]])
    Corners = namedtuple("Corners", "ul ur lr ll")
    return Corners(*apply_tform(tform, corners))


def convert_transform(tform):
    """Convert a transform into arguments for VIPS affine.

    The transformation matrices in the coregistation file are defined

        | row' | = | q  r  s | | row |
        | col' | = | t  u  v | | col |
        |  1   | = | 0  0  1 | |  1  |

    The VIPS image.affine method takes a `matrix` argument [a, b, c, d] and
    offset arguments `odx` and `ody` such that

        | col' | = | a  b | | col | + | odx |
        | row' | = | c  d | | row |   | ody |

    Given the first matrix, return arguments for the image.affine method.
    """
    matrix = [tform[1, 1], tform[1, 0], tform[0, 1], tform[0, 0]]
    odx = tform[1, 2]
    ody = tform[0, 2]
    return matrix, odx, ody


def mosaick(
    panels: list[pyvips.Image], tforms: list[np.ndarray]
) -> tuple[pyvips.Image, list[int]]:
    """Combine a list images according to a list of transforms.

    Parameters
    ----------
    panels
        The images to mosaick in left-to-right order.
    tforms
        Homogenous transformation matrices for each panel that project from
        (row, col) in the source image to (row', col') in the result.

    Notes
    -----
    The size of the result is automatically determined by the largest row and
    column coordinates of the projected image. If input pixels are projected to
    negative row or column coordinate in the result, they are lost: the output
    only expands in the positive direction.

    Returns
    -------
    result
        The mosaicked image.
    split_columns
        The columns in result image where the result switches from one panels
        to the next.
    """
    if len(panels) != len(tforms):
        raise ValueError("There should be one transform per panel.")

    # Calculate the corners of each panel in the final image.
    panel_corners = [get_tformed_corners(t, p) for (t, p) in zip(tforms, panels)]

    # Caculate the size of the result image based on the maximum extents of the
    # transformed panel images.
    max_row = max(corner[0] for corners in panel_corners for corner in corners)
    max_col = max(corner[1] for corners in panel_corners for corner in corners)
    num_rows = int(np.ceil(max_row)) + 1
    num_cols = int(np.ceil(max_col)) + 1

    # Warp the panels into place in an image the size of the output image. We
    # won't end up using pixels from the left and right edges where panels
    # meet, so we don't need to be concerned with edge effects in the
    # interpolation method.
    panels_tformed = []
    for panel, tform in zip(panels, tforms):
        matrix, odx, ody = convert_transform(tform)
        panels_tformed.append(
            panel.affine(
                matrix,
                interpolate=pyvips.Interpolate.new("bicubic"),
                oarea=[0, 0, num_cols, num_rows],
                odx=odx,
                ody=ody,
            )
        )

    # Determine the columns where the output image switches from one panel to
    # the next by using the midpoint of each overlap region. These values will
    # define half-open column intervals.
    split_columns = [0]
    for left, right in zip(panel_corners, panel_corners[1:]):
        mid = (left.ur + left.lr + right.ul + right.ll) / 4.0
        split_columns.append(mid.astype(int)[1])
    split_columns.append(num_cols)

    # Crop the images to the calculated columns.
    panels_cropped = []
    for panel, left, right in zip(panels_tformed, split_columns, split_columns[1:]):
        panels_cropped.append(panel.crop(left, 0, right - left, num_rows))

    # Join the cropped images.
    result = pyvips.Image.black(num_cols, num_rows)
    for panel, left in zip(panels_cropped, split_columns):
        result = result.insert(panel, left, 0)

    return result, split_columns[1:-1]
