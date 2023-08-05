# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
from pathlib import Path

import click
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import pandas as pd
from xmlhelpy import Choice
from xmlhelpy import option
from xmlhelpy import TokenList

from .main import plot


@plot.command(
    description="A plot node for plotting columns from a text file using matplotlib;"
    " for more colums using ',' as separator."
)
@option(
    "filename",
    char="F",
    description="Name of the input file",
    excludes=["filenames_list"],
)
@option(
    "filenames_list",
    char="L",
    description="Name of the input file",
    param_type=TokenList,
    excludes=["filename"],
    requires=["plotoutput"],
)
@option(
    "separator",
    char="s",
    description="Columns separator",
    default="tab",
    param_type=Choice(["space", "tab", "comma"]),
)
@option(
    "plotoutput",
    char="o",
    default=None,
    description="Resulting plot, the format is controlled by file extension: *.svg, "
    "*.pdf, *.png, ...",
)
@option(
    "output_format",
    char="q",
    default="pdf",
    description="Resulting plot format, the format is controlled by file extension: "
    "*.svg, *.pdf, *.png, ...",
    param_type=Choice(["pdf", "svg", "eps", "png", "pgf", "ps", "raw", "rgba", "svgz"]),
)
@option(
    "columns",
    char="u",
    required=False,
    description="Specified columns from input file to be printed, e.g. -u 2:3 for plot "
    "columns 3 to 4 in reading file",
)
@option(
    "parameter_x",
    char="x",
    default=None,
    description="Parameter for the x axis",
)
@option(
    "parameter_y",
    char="y",
    default=None,
    description="Parameter for the y axis",
)
@option(
    "keylabel",
    char="l",
    default=None,
    description="Key label for the curve, 'auto' is automatic using the colums, when "
    "using the -x and -y option",
)
@option(
    "xlabel",
    char="a",
    default=None,
    description="X label for the plot.",
)
@option(
    "ylabel",
    char="b",
    default=None,
    description="Y label for the plot.",
)
@option(
    "title",
    char="t",
    default=None,
    description="Title for the plot.",
)
@option(
    "color",
    char="c",
    default="black",
    description="Color for the plot.",
)
@option(
    "linestyle",
    char="z",
    default="-",
    description="Linestyle for the plot, for example '-', '--', '-.', ':', 'None', "
    "'solid', 'dashed', 'dashdot', 'dotted'.",
)
@option(
    "linewidth",
    char="w",
    default="1",
    description="Linewidth for the plot.",
)
@option(
    "equal_axis",
    char="e",
    default=None,
    description="Equals the scale of the axis.",
)
@option(
    "x_lim",
    char="m",
    default=None,
    description="Limits of the x axis.",
)
@option(
    "y_lim",
    char="n",
    default=None,
    description="Limits of the y axis.",
)
@option(
    "x_scale",
    char="i",
    default=None,
    description="Scale of the x-axis",
    param_type=Choice(["linear", "log", "symlog."]),
)
@option(
    "y_scale",
    char="j",
    default=None,
    description="Scale of the y-axis.",
    param_type=Choice(["linear", "log", "symlog"]),
)
@option(
    "x_minor_ticks",
    char="f",
    default="1",
    description="n-1 number of small ticks on x-axis.",
)
@option(
    "y_minor_ticks",
    char="g",
    default="1",
    description="n-1 number of small ticks on y-axis.",
)
@option(
    "major_grid",
    char="H",
    is_flag=True,
    description="Major grid on, if used.",
)
@option(
    "minor_grid",
    char="h",
    is_flag=True,
    description="Minor grid on, if used.",
)
@option(
    "position",
    char="p",
    default="best",
    description="Position of the legend.",
    param_type=Choice(
        ["best", "upper left", "upper right", "lower left", "lower right"]
    ),
)
@option(
    "marker",
    char="M",
    default=".",
    description="Marker type.",
    param_type=Choice([".", "o", "v", "^", "<", ">", "x"]),
)
def plot_matplotlib(
    filename,
    filenames_list,
    separator,
    plotoutput,
    output_format,
    columns,
    parameter_x,
    parameter_y,
    keylabel,
    xlabel,
    ylabel,
    title,
    color,
    linestyle,
    linewidth,
    position,
    equal_axis,
    x_lim,
    y_lim,
    x_scale,
    y_scale,
    x_minor_ticks,
    y_minor_ticks,
    major_grid,
    minor_grid,
    marker,
):
    """A plot node for plotting columns from a text file using matplotlib."""

    if filename is None and filenames_list is None:
        click.echo("Please specify either a file or a filelist as input.")
        sys.exit(1)

    if separator == "tab":
        separator = "\t"
    elif separator == "space":
        separator = r"\s+"
    else:
        separator = ","

    if plotoutput is None:
        plotoutput = Path(filename).stem
        plotoutput = f"{plotoutput}." + output_format
    else:
        plotoutput = f"{plotoutput}." + output_format

    if columns is None:
        if (parameter_x or parameter_y) is None:
            click.echo("Please specify the column to plot.")
            sys.exit(1)

    fig = plt.figure()
    ax = fig.subplots()

    if filenames_list:
        for file in filenames_list:

            if not os.path.isfile(file):
                click.echo("File '{file}' does not exists.")
                sys.exit(1)

            data = pd.read_csv(file, sep=separator)
            x_data_plot = data.iloc[:, int(columns.split(":")[0])]
            y_data_plot = data.iloc[:, int(columns.split(":")[1])]
            plt.plot(x_data_plot, y_data_plot, label=str(file))
        plt.legend(loc=position)

    else:
        data = pd.read_csv(filename, sep=separator)

        colors_list = color.split(",")
        linestyle_list = linestyle.split(",")
        linewidth_list = linewidth.split(",")
        markers_list = marker.split(",")

        if (keylabel is not None) and (keylabel != "auto"):
            keylabel_list = keylabel.split(",")

        if columns is not None:
            columns_list_x = columns.split(",")
        else:
            columns_list_x = parameter_x.split(",")
            columns_list_y = parameter_y.split(",")

        for loop_number, loop_value in enumerate(columns_list_x):
            if columns is not None:
                x_data_plot = data.iloc[:, int(loop_value.split(":")[0])]
                y_data_plot = data.iloc[:, int(loop_value.split(":")[1])]
            else:
                x_data_plot = data[loop_value]
                y_data_plot = data[columns_list_y[loop_number]]

            if len(colors_list) > 1:
                color_plot = colors_list[loop_number]
            else:
                color_plot = color

            if len(markers_list) > 1:
                marker_plot = markers_list[loop_number]
            else:
                marker_plot = marker

            if len(linestyle_list) > 1:
                linestyle_plot = linestyle_list[loop_number]
            else:
                linestyle_plot = linestyle

            if len(linewidth_list) > 1:
                linewidth_plot = linewidth_list[loop_number]
            else:
                linewidth_plot = linewidth
            if (keylabel != "auto") and (keylabel is not None):
                keylabel_plot = keylabel_list[loop_number]
            elif (keylabel == "auto") and (columns is None):
                keylabel_plot = columns_list_y[loop_number]
            else:
                keylabel_plot = None

            plt.plot(
                x_data_plot,
                y_data_plot,
                label=keylabel_plot,
                color=color_plot,
                linestyle=linestyle_plot,
                linewidth=linewidth_plot,
                marker=marker_plot,
            )

    if columns is None:
        if len(columns_list_y) < 2:
            if xlabel is None:
                xlabel = parameter_x
            if ylabel is None:
                ylabel = parameter_y

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if keylabel is not None:
        plt.legend(loc=position)

    if equal_axis is not None:
        plt.axis("equal")
    if title is not None:
        plt.title(title)
    if x_lim is not None:
        plt.xlim(int(x_lim.split(",")[0]), int(x_lim.split(",")[1]))
    if y_lim is not None:
        plt.ylim(int(y_lim.split(",")[0]), int(y_lim.split(",")[1]))
    if x_scale is not None:
        plt.xscale(x_scale)
    if y_scale is not None:
        plt.yscale(y_scale)

    ax.xaxis.set_minor_locator(tck.AutoMinorLocator(int(x_minor_ticks)))
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator(int(y_minor_ticks)))

    if minor_grid:
        plt.grid(True, which="minor")
    if major_grid:
        plt.grid(True, which="major")

    plt.savefig(plotoutput)
    plt.close("all")

    click.echo(f"Created file {plotoutput}")
