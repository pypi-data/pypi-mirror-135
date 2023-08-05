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
import os
import subprocess
import sys

from xmlhelpy import argument
from xmlhelpy import option

from .main import misc


@misc.command(description="Octave node for using octave scripts")
@argument("file")
@option(
    "exec-path",
    var_name="path",
    char="p",
    description="Set the execution path in which to look for the octave script",
)
@option("gui", description="Force octave to open the gui", is_flag=True)
@option(
    "variables",
    char="v",
    description="Variables passed to the script. Expects the variables as a string"
    " separated by ,",
)
def octave(file, path, variables, gui):
    """Wrapper node for Octave."""

    cmd = ["octave"]

    if gui:
        cmd += ["--force-gui"]
    if path:
        exec_file = [os.path.join(path, file)]
        cmd += exec_file
    if variables:
        var_string = variables.strip('"').strip("'")
        var_list = var_string.split(",")
        for var in var_list:
            cmd += [var]

    sys.exit(subprocess.call(cmd))
