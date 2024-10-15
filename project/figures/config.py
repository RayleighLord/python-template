from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from ..utils.colors import GREY_BACKGROUND
from mpl_toolkits.mplot3d.axis3d import Axis
from ..utils.utils import check_and_create_directory


__all__ = [
    "figure_features",
    "signature",
    "add_grid",
    "custom3d_plots",
    "save_figure",
]


def figure_features(
    tex=True,
    font="serif",
    dpi=250,
    background="white",
    use_amsmath=True,
    use_physics=True,
    left=0.15,
    three_d_mode=False,
):
    """
    Sets basic figure parameters

    Parameters:
        - tex: bool to indicate the use of LaTeX through a native compiler
        - font: string to select the font used in the figure
        - dpi: dots per inch in the image saved (180 recommended for
        high quality figures)
        - background: string to select the color of the background
        ['black', 'grey, 'white']
        - use_amsmath: bool to use the known asmath LaTeX package
        - use_physics: bool to use the known physics LaTeX package
    """

    assert background in [
        "black",
        "grey",
        "white",
    ], "That is not a valid color for the background"

    if background == "black":

        plt.style.use("dark_background")

    elif background == "grey":
        plt.rcParams["axes.facecolor"] = GREY_BACKGROUND
        plt.rcParams["figure.facecolor"] = GREY_BACKGROUND
        plt.rcParams["savefig.facecolor"] = GREY_BACKGROUND

    elif background == "white":
        pass

    if use_amsmath:
        plt.rc("text.latex", preamble=r"\usepackage{amsmath}")

    if use_physics:
        plt.rc("text.latex", preamble=r"\usepackage{physics}")

    plt.rcParams.update(
        {
            "font.size": 16,
            "font.family": font,
            "text.usetex": tex,
            "figure.subplot.top": 0.9,
            "figure.subplot.right": 0.9,
            "figure.subplot.left": left,
            "figure.subplot.hspace": 0.4,
            "savefig.dpi": dpi,
            "savefig.format": "png",
            "axes.titlesize": 18,
            "axes.labelsize": 22,
            "axes.axisbelow": True,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 10,
            "xtick.minor.size": 5,
            "xtick.major.pad": 7.5,
            "xtick.minor.pad": 7.5,
            "ytick.major.pad": 7.5,
            "ytick.minor.pad": 7.5,
            "ytick.major.size": 10,
            "ytick.minor.size": 5,
            "xtick.labelsize": 22,
            "ytick.labelsize": 22,
            "legend.fontsize": 18,
            "legend.framealpha": 0.8,
            "figure.titlesize": 20,
            "lines.linewidth": 2,
            "ytick.right": True,
            "xtick.top": True,
        }
    )

    if three_d_mode:

        def _get_coord_info_new(self, renderer):
            mins, maxs, cs, deltas, tc, highs = self._get_coord_info_old(
                renderer
            )
            correction = deltas * [1.0 / 4, 1.0 / 4, 1.0 / 4]
            mins += correction
            maxs -= correction
            return mins, maxs, cs, deltas, tc, highs

        if not hasattr(Axis, "_get_coord_info_old"):
            # noinspection PyProtectedMember
            Axis._get_coord_info_old = Axis._get_coord_info

        Axis._get_coord_info = _get_coord_info_new

        plt.rcParams.update(
            {
                "xtick.major.pad": 2.5,
                "xtick.minor.pad": 2.5,
                "ytick.major.pad": 2.5,
                "ytick.minor.pad": 2.5,
            }
        )


def signature(fig, sign="@RayleighLord", color="w", sign_position="DR"):
    """
    Sets a custom signature for the animations

    Parameters:
        - fig: figure to add the signature
        - sign: string with the signature to include
        - color: color of the signature
        - sign_position: position of the signature in the figure
        {'DR': Down Right,
         'DL': Down Left,
         'UR': Upper Right,
         'UL': Upper Left}
    """
    if sign_position == "DR":
        sign_position = [0.775, 0.025]

    elif sign_position == "DL":
        sign_position = [0.025, 0.025]

    elif sign_position == "UR":
        sign_position = [0.775, 0.925]

    elif sign_position == "UL":
        sign_position = [0.025, 0.925]

    else:
        raise Exception(
            "Invalid signature position. Choose from ['LR', 'LL', 'UR', 'UL']."
        )

    ax_position = sign_position + [0.2, 0.1]

    ax_name = fig.add_axes(ax_position, xlim=(0, 1), ylim=(0, 1))
    ax_name.text(0, 0.1, sign, color=color, size=15, alpha=0.7)
    ax_name.axis("off")


def add_grid(ax, lines=True, locations=None):
    """
    Add gridlines and markers to the a plot
    Args:
        ax: The ax object in which to apply the grid
        lines: Set to True to show grid lines and False otherwise
        locations: locations of multiple locator (xminor, xmajor, yminor,
        ymajor)

    Returns:

    """

    if lines:
        ax.grid(lines, alpha=0.5, which="minor", ls=":")
        ax.grid(lines, alpha=0.7, which="major")

    if locations is not None:

        assert (
            len(locations) == 4
        ), "Invalid entry for the locations of the markers"

        xmin, xmaj, ymin, ymaj = locations

        ax.xaxis.set_minor_locator(MultipleLocator(xmin))
        ax.xaxis.set_major_locator(MultipleLocator(xmaj))
        ax.yaxis.set_minor_locator(MultipleLocator(ymin))
        ax.yaxis.set_major_locator(MultipleLocator(ymaj))


def custom3d_plots(
    ax, color="w", coordinates=None, lines=True, locations=None
):
    """
    Add gridlines and markers to the a plot
    Args:
        ax: The ax object in which to apply the grid
        color: Set the color of the panes of the plot
        coordinates: Tuple (distance, elevation, azimut) to customize the
        view of the 3d plot
        lines: Set to True to show grid lines and False otherwise
        locations: locations of multiple locator (xminor, xmajor, yminor,
        ymajor, zminor, zmajor)

    Returns:

    """

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis.pane.set_edgecolor(color)
    ax.yaxis.pane.set_edgecolor(color)
    ax.zaxis.pane.set_edgecolor(color)

    if coordinates is not None:
        ax.dist, ax.elev, ax.azim = coordinates

    if lines:
        ax.grid(lines, alpha=0.5, which="minor", ls=":")
        ax.grid(lines, alpha=0.7, which="major")

    if locations is not None:

        assert (
            len(locations) == 6
        ), "Invalid entry for the locations of the markers"

        xmin, xmaj, ymin, ymaj, zmin, zmaj = locations

        ax.xaxis.set_minor_locator(MultipleLocator(xmin))
        ax.xaxis.set_major_locator(MultipleLocator(xmaj))
        ax.yaxis.set_minor_locator(MultipleLocator(ymin))
        ax.yaxis.set_major_locator(MultipleLocator(ymaj))
        ax.zaxis.set_minor_locator(MultipleLocator(zmin))
        ax.zaxis.set_major_locator(MultipleLocator(zmaj))


def save_figure(route, name):

    check_and_create_directory(route)
    plt.savefig(f"{route}{name}.png")
