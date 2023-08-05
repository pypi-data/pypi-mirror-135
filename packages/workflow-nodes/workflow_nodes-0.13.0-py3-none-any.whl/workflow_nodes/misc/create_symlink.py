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
from pathlib import Path

from xmlhelpy import option

from .main import misc


@misc.command(description="Creates a symlink with given name and path")
@option(
    "target",
    char="t",
    description="Symlink target (default is current directory)",
    required=False,
)
@option(
    "path",
    char="p",
    description="Path where the symlink should be stored.",
    required=False,
)
@option("name", char="n", description="Name of the Desktop entry", required=True)
@option(
    "force",
    char="f",
    description="Force symlink creation (overwrite if exists)",
    is_flag=True,
)
def create_symlink(*args, **kwargs):
    """Create a symlink."""

    target = Path().cwd()  # current directory
    if kwargs["target"]:
        target = kwargs["target"]
    symlink_path = Path.cwd()
    if kwargs["path"]:
        symlink_path = Path(kwargs["path"]).expanduser()
    name = kwargs["name"]
    force = kwargs["force"]

    symlink_path = symlink_path.joinpath(name)
    print(f"Creating symlink {symlink_path} pointing to {target}")
    cmd = ["ln", "-s"]
    if force:
        print("Overwriting if existing")
        cmd += ["-fn"]  # ln's -f argument only works together with -n (no dereference)
    cmd += [str(target), str(symlink_path)]
    exit_code = subprocess.call(cmd)
    print("done")
    sys.exit(exit_code)
