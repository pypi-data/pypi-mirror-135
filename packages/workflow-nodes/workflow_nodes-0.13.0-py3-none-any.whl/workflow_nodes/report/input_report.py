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

from pylatex import NoEscape
from xmlhelpy import option

from .main import report


@report.command()
@option("path", char="p", required=True, description="Name of the Latex file")
def input_report(*args, **kwargs):
    """A program to input a latex file."""

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

    doc.append(NoEscape(r"\input{%s}" % kwargs["path"]))

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
