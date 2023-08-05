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
import os.path
import subprocess
import sys

from xmlhelpy import option

from .main import report


@report.command()
@option("file", char="p", required=True, description="Name of the Latex file")
def compile_latex_report(*args, **kwargs):
    """Compile a latex document."""

    path = kwargs["file"]

    cmd = ["pdflatex"]
    cmd.append("-synctex=1")
    cmd.append("-interaction=nonstopmode")
    cmd.append("--shell-escape")
    cmd.append(kwargs["file"])
    # Do not write to stdout to keep output intact for piping.
    print(" ".join(cmd), file=sys.stderr)
    # Run the latex command in the right folder.
    subprocess.call(cmd, cwd=os.path.dirname(path))
