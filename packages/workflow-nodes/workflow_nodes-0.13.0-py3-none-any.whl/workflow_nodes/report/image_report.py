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

from pylatex import Figure
from pylatex import NoEscape
from pylatex import Section
from xmlhelpy import Float
from xmlhelpy import option

from .main import report


@report.command()
@option("path", char="p", required=True, description="Path to the image to display")
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
@option(
    "imagewidth",
    char="w",
    default=0.5,
    description="Specifies the width of the images.",
    param_type=Float,
)
def image_report(*args, **kwargs):
    """A program to embed an image into a latex snippet."""

    path = kwargs["path"]
    caption = kwargs["caption"]
    section = kwargs["section"]
    imagewidth = kwargs["imagewidth"]
    imagewidth = f"{imagewidth}\\textwidth"

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

        def _add_figure(doc):
            with doc.create(Figure(position="h!")) as figure:
                figure.add_image(path, width=NoEscape(imagewidth))
                if caption is not None:
                    figure.add_caption(caption)

        if section is not None:
            with doc.create(Section(section)):
                _add_figure(doc)
        else:
            _add_figure(doc)

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
