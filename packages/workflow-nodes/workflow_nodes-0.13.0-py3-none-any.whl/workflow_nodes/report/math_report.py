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

from pylatex import Alignat
from pylatex import NoEscape
from xmlhelpy import option

from .main import report


@report.command()
@option("formula", char="f", default=None, description="Latex code of the formula.")
def math_report(*args, **kwargs):
    """A program to embed a formula into a latex snippet."""

    formula = kwargs["formula"]

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(NoEscape(formula))

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
