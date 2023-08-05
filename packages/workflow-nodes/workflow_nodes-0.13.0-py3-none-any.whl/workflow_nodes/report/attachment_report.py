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
from pylatex import Section
from xmlhelpy import option

from .main import report


@report.command()
@option("name", char="n", description="The name of the excel file (must be unique)")
@option("file", char="f", description="The file to attach", required=True)
@option("section", char="s", default="Attachments", description="Section name")
def attachment_report(*args, **kwargs):
    """Add a file as attachment to the report."""

    with open(".report.obj", mode="rb") as f:
        doc = pickle.load(f)

        with doc.create(Section(kwargs["section"])):
            if kwargs["name"] is not None:
                # attachment with name
                doc.append(
                    NoEscape(
                        r"\textattachfile{{./{}}}{{{}}}".format(
                            kwargs["file"], kwargs["name"]
                        )
                    )
                )
            else:
                # attachment without name, print an icon instead
                doc.append(
                    NoEscape(r"\attachfile[icon=Paperclip]{./%s}" % kwargs["file"])
                )

    with open(".report.obj", mode="wb") as f:
        pickle.dump(doc, f)
