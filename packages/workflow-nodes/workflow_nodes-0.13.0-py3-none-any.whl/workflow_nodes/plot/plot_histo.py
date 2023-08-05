# Copyright 2021 Karlsruhe Institute of Technology
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
import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import Integer
from xmlhelpy import option

from .main import plot


@plot.command(example='"skeleton_1.dat,skeleton_2.dat" -p histogram -q .pdf -u 4,4')
@argument(
    "filename",
    required=True,
    description="Name(s) of the input file(s).",
)
@option(
    "plotname",
    char="p",
    default=None,
    description="Name of the resulting plot.",
)
@option(
    "output_format",
    char="q",
    default=".pdf",
    description="Resulting plot format, the format is controlled by file extension: "
    "*.svg, *.pdf, *.png, ...",
    param_type=Choice(
        [".pdf", ".svg", ".eps", ".png", ".pgf", ".ps", ".raw", ".rgba", ".svgz"]
    ),
)
@option(
    "columns",
    char="u",
    description="Specified columns to be printed from input file; if more than"
    " one file is processed, follow the order of the inputfile e.g."
    " -u 2,3; the first column number belongs to the first inputfile, etc..",
)
@option(
    "user_bins",
    char="w",
    default=None,
    param_type=Integer,
    description="Number of bins for the histogramm. If not specified"
    " an optimum value is calculated.",
)
@option(
    "parameter_x",
    char="x",
    default=None,
    description="Parameter name for the distribution.",
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
    default="probability density, PDF(x)",
    description="Y label for the plot.",
)
@option(
    "separator",
    char="s",
    description="Columns separator",
    default="comma",
    param_type=Choice(["space", "tab", "comma"]),
)
@option(
    "title",
    char="t",
    default=None,
    description="Title for the plot",
)
def plot_histo(
    filename,
    plotname,
    output_format,
    columns,
    user_bins,
    parameter_x,
    xlabel,
    ylabel,
    separator,
    title,
):
    """A node for plotting a histogram using matplotlib.

    Several distributions from different inputfiles can be plotted
    in one histogram. A PDF from the data is fitted as well.
    """

    filenamelist = filename.split(",")

    if separator == "tab":
        separator = "\t"
    elif separator == "space":
        separator = r"\s+"
    else:
        separator = ","

    if plotname is None:
        plotname = Path(filename).stem
        plotname = f"{plotname}_plot."

    if columns is None and parameter_x is None:
        print("Specify the column number or column name to plot")
        sys.exit(1)

    r = lambda: random.randint(0, 255)

    for i, listentry_filename in enumerate(filenamelist):
        data = pd.read_csv(
            listentry_filename, sep=separator, engine="python", skipinitialspace=True
        )

        if parameter_x is None:
            column_name = data.columns[int(columns.split(",")[i]) - 1]
        else:
            number = data.columns.get_loc(parameter_x.split(",")[i])
            column_name = data.columns[number]

        x = data[column_name]
        q25, q75 = np.percentile(x, [25, 75])
        bin_width = 2 * (q75 - q25) * len(x) ** (-1 / 3)

        if user_bins is None:
            bins = round((x.max() - x.min()) / bin_width)
            print(f"Number of calculated bins for file {listentry_filename} : {bins}")
        else:
            bins = user_bins

        _, bins, _ = plt.hist(
            x,
            bins,
            color=f"#{r():02x}{r():02x}{r():02x}",
            alpha=0.7,
            density=1,
            label=f"{listentry_filename}",
            rwidth=0.85,
        )

        mu, sigma = norm.fit(x)
        best_fit_line = norm.pdf(bins, mu, sigma)
        label_fit = f"FIT-{listentry_filename}: mu = {mu:.2f},  std = {sigma:.2f}"
        plt.plot(bins, best_fit_line, color="r", lw=2, label=label_fit)

        if xlabel is not None:
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)

        plt.legend(bbox_to_anchor=(1, 1))
        if title is not None:
            plt.title(title)

    plt.savefig(plotname + output_format, bbox_inches="tight")
    plt.close("all")
    print(f"Created file {plotname}{output_format}")
