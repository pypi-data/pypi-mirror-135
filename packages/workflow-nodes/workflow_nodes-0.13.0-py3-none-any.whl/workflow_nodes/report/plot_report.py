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
import pickle

import matplotlib
import matplotlib.pyplot as plt
from pylatex import Figure
from pylatex import NoEscape
from pylatex import Section

matplotlib.use("Agg")  # To use the headless backend

from xmlhelpy import option
from .main import report


@report.command()
@option("path", char="p", required=True, description="Path to the data file to plot")
@option(
    "caption",
    char="c",
    default=None,
    description="Caption of the figure wrapping this image.",
)
@option(
    "section",
    char="s",
    default=None,
    description="Section title. Inserts no section if not specified.",
)
def plot_report(caption, section, path, width=r"0.8\textwidth"):
    """A program to embed a plot into a latex snippet."""

    def remove_quotes(x):
        return x if not isinstance(x, str) != str else x.strip("'")

    caption = remove_quotes(caption)
    section = remove_quotes(section)

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

    def _add_figure(doc):
        with doc.create(Figure(position="htb")) as plot:
            with open(path, encoding="utf-8") as f:
                content = f.readlines()
            content = [float(x.strip()) for x in content]
            y = content
            x = list(range(len(content)))

            plt.plot(x, y)
            plot.add_plot(width=NoEscape(width))
            if caption is not None:
                plot.add_caption(caption)

    if section is not None:
        with doc.create(Section(section)):
            _add_figure(doc)
    else:
        _add_figure(doc)

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
