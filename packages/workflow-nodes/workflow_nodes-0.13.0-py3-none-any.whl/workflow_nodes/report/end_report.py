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

from xmlhelpy import option

from .main import report


@report.command()
@option(
    "output",
    char="o",
    default="output.pdf",
    description="Path of the pdf file to generate.",
)
def end_report(*args, **kwargs):
    """Finish a report and generate the pdf."""

    output = kwargs["output"]

    # workaround because Document.generate_pdf always adds '.pdf' to the file name
    if output.endswith(".pdf"):
        output = output[: -len(".pdf")]

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)
        doc.generate_pdf(output, clean_tex=False)
        doc.generate_tex("raw.tex")
