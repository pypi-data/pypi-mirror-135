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

from xmlhelpy import option

from .main import system


@system.command(
    description="Wrapper node for bc - An arbitrary precision calculator language"
)
@option("file", description="file", required=False)
@option("interactive", char="i", description="Force interactive mode.", is_flag=True)
@option(
    "mathlib", char="l", description="Define the standard math library.", is_flag=True
)
@option(
    "warn",
    char="w",
    description="Give warnings for extensions to POSIX bc.",
    is_flag=True,
)
@option(
    "standard",
    char="s",
    description="Process exactly the POSIX bc language.",
    is_flag=True,
)
@option(
    "quiet",
    char="q",
    description="Do not print the normal GNU bc welcome.",
    is_flag=False,
)
def bc(*args, **kwargs):
    """Wrapper node for bc."""

    file = kwargs["file"]
    interactive = kwargs["interactive"]
    mathlib = kwargs["mathlib"]
    warn = kwargs["warn"]
    standard = kwargs["standard"]
    quiet = kwargs["quiet"]

    cmd = ["bc"]
    flags_str = "-"
    if interactive:
        flags_str += "i"
    if mathlib:
        flags_str += "l"
    if warn:
        flags_str += "w"
    if standard:
        flags_str += "s"
    if quiet:
        flags_str += "q"

    if len(flags_str) > 1:
        cmd += flags_str
    if file and file is not None:
        cmd += file
    # Do not write to stdout to keep output intact for piping.
    print(" ".join(cmd), file=sys.stderr)
    sys.exit(subprocess.call(cmd))
