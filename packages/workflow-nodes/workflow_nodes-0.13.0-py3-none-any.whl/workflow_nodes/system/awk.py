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
import subprocess
import sys

from xmlhelpy import argument
from xmlhelpy import option

from .main import system


@system.command()
@option("assign", char="v", description="", required=False)
@argument("expression", description="expression")
@argument("file", description="file", required=False)
def awk(*args, **kwargs):
    """Wrapper node for awk."""

    cmd = ["awk"]
    if "assign" in kwargs and kwargs["assign"] is not None:
        cmd.append("-v")
        cmd.append(kwargs["assign"])
    cmd.append(kwargs["expression"])
    if "file" in kwargs and kwargs["file"] is not None:
        cmd.append(kwargs["file"])
    # Do not write to stdout to keep output intact for piping.
    print(" ".join(cmd), file=sys.stderr)
    sys.exit(subprocess.call(cmd))
