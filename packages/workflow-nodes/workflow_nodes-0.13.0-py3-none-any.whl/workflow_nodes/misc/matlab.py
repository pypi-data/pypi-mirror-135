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
import subprocess
import sys

from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import option

from .main import misc


@misc.command(description="Matlab node for using Matlab scripts")
@argument(
    "file",
)
@option(
    "startup-folder",
    char="f",
    description="Change the matlab startup folder to defined path",
)
@option(
    "execution-mode",
    char="m",
    var_name="mode",
    description="Choose the desired execution mode:"
    " single=single execution of script in bash"
    " and Matlab closes automatically after runthrough;"
    " bash=bash execution of script and matlab stays open after runthrough;"
    " desktop=execution of script in Matlab desktop"
    " and matlab stays open after runthrough",
    default="single",
    param_type=Choice(["single", "bash", "desktop"]),
)
def matlab(file, startup_folder, mode):
    """Wrapper node for Matlab."""

    cmd = ["matlab"]
    if startup_folder:
        cmd += ["-sd", startup_folder]

    if mode == "single":
        cmd += ["-batch", file]
    elif mode == "bash":
        cmd += ["-nodesktop -nosplash -r", file]
    elif mode == "desktop":
        cmd += ["-r", file]

    print(" ".join(cmd), file=sys.stderr)
    sys.exit(subprocess.call(cmd))
