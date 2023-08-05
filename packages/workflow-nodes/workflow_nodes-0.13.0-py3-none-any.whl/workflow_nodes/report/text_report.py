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

from pylatex import Section
from xmlhelpy import option

from .main import report


@report.command()
@option("text", char="t", default="No text specified", description="Text to insert")
@option("section", char="s", default=None, description="Latex Section")
def text_report(*args, **kwargs):
    """A program to embed text into a latex report."""

    text = kwargs["text"]
    section = kwargs["section"]

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

    if section is not None:
        with doc.create(Section(section)):
            doc.append(text)

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
